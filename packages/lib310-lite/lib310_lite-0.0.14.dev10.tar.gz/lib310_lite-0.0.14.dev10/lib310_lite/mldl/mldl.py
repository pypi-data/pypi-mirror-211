import numpy as np
import random
import time
import asyncio
import pandas as pd
from threading import Thread, Event
from queue import Queue
import concurrent.futures
from bounded_pool_executor import BoundedThreadPoolExecutor
import dask.dataframe as dd
from ..bigquery.client import Client as BigQueryClient
from ..bigquery.constants import FileFormat
import hashlib

# PGSQL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models.SeqLangModel import SeqLangModel, SeqLang300Model, SeqLangT10Model, SeqLang300T10Model
from .models.InteractionModel import InteractionModel, Interaction300Model, InteractionT10Model, Interaction300T10Model

import time


class MLDL:

    __TRAIN = 'TRAIN'
    __TEST = 'TEST'
    __VAL = 'VAL'
    __MAIN = 'MAIN'
    __INTERACTION = 'INTERACTION'
    __PARTS = {__INTERACTION: 1}

    def __init__(self, db_url: str,
                 cache_size: int = 50,
                 num_threads: int = 10,
                 random_seed: int = time.time()
                 ):
        random.seed(random_seed)
        self.engine = create_engine(db_url, pool_size=3 * num_threads, max_overflow=6 * num_threads, pool_recycle=60)
        self.Session = sessionmaker(bind=self.engine)

        self.bq_client = BigQueryClient()

        # this is the pool of samples row_id
        self.pool = []
        # this is the maximum number of requests we fetch sooner from the database
        self.max_queue_size = cache_size
        # this is the number of threads we use to fetch data from the database
        self.num_threads = num_threads
        # this is the key that we know MLDL requests are same or not if it changes we need to fetch new data
        self.queue_key = None
        # this is the key shows that pool is still valid or not
        self.pool_key = None
        # this is the queue that cache the responses
        self.responses_queue = Queue(self.max_queue_size)
        # this is the queue that cache index of requests
        self.requests_queue = Queue(self.max_queue_size * 2)
        # this is the thread that we use to fill the queue
        self.filler_thread = None
        # this is the event that we use to kill the filler thread
        self.kill_event = Event()

        # Create an event loop
        loop = asyncio.get_event_loop()

        # this is the thread that we use to fill request queue
        self.fill_request_thread = None
        # this kill fill requests thread
        self.kill_fill_requests_event = Event()

        # pool values
        self.max_length = 10000000
        self.token_size = -1
        self.stage = self.__TRAIN
        self.interactions_count = -1
        self.query = None

    def create_pool(self, max_length: int = 300, min_num_feature: int = 10, stage: str = __TRAIN, interactions_count: int = -1, query: str = None):
        self.max_length = max_length
        self.token_size = min_num_feature
        self.stage = stage.upper()
        self.interactions_count = interactions_count
        self.query = query

        if query is not None and self.pool_key != query:
            self.pool_key = hashlib.sha1(query.encode('utf-8')).hexdigest()
            res = self.bq_client.cache_query(
                query=query,
                name=self.pool_key,
                destination_format=FileFormat.CSV
            )
            ddf = dd.read_csv(res['uri'])
            df = ddf.compute()
            self.pool = df['row_id'].tolist()

        elif len(self.pool) == 0 or not self.pool_key or self.pool_key != f'{max_length}_{min_num_feature}_{stage}_{interactions_count}':
            table = '1_uniprot.pg_lang5'
            self.pool_key = f'{max_length}_{min_num_feature}_{stage}_{interactions_count}'
            tmp_query = f"SELECT row_id FROM `{table}` WHERE len <= {max_length} and token_size >= {min_num_feature} and stage = '{stage}'"
            if interactions_count > 0:
                tmp_query += f" and interactions_count >= {interactions_count}"
            res = self.bq_client.cache_query(
                query=tmp_query,
                name=f'{max_length}_{min_num_feature}_{stage}',
                destination_format=FileFormat.CSV
            )
            # print(res)
            ddf = dd.read_csv(res['uri'])
            df = ddf.compute()
            self.pool = df['row_id'].tolist()
        # shuffle the pool to make sure that we have a random pool
        random.shuffle(self.pool)
        return self.pool

    def get_batch(self, num: int, parts: dict = None):
        """
        Get a batch of data from the database with regard to the length of the sequence and the number of features
        It also start the background thread to fill the caches and queue
        :param num: number of samples
        :param parts: the parts of the data that we want to fetch
        :return: a pandas dataframe
        """

        qk = f'{num}_{self.max_length}_{self.token_size}_{self.stage}'
        if self.query is not None:
            self.max_length = 10000000
            self.token_size = -1
            self.stage = self.__TRAIN
            self.interactions_count = -1
            hq = hashlib.sha1(self.query.encode('utf-8')).hexdigest()
            qk = f'{num}_{hq}'

        if parts is None:
            parts = MLDL.__PARTS

        # we check queue key to see if the query is the same or not
        hit = self.queue_key == qk
        if hit:
            # HIT
            return self.responses_queue.get()
        # MISS
        # killing the previous thread
        self.terminate()

        # fill the index in request queue
        self.fill_request_thread = Thread(target=self.fill_request_queue, args=[num])
        self.fill_request_thread.start()

        # generate new key
        self.queue_key = qk

        # start new thread
        self.filler_thread = Thread(target=self.filler, args=(num, parts))
        self.filler_thread.start()

        # if we do not put this it could effect on the performance of the program because of the racing between threads
        time.sleep(3)

        return self.fetch_sample(num, parts)

    def filler(self, num: int, parts: dict = None):
        """
        This function is used to fill the queue with data then get batch read data from the queue
        :param num: number of samples
        :param parts: the parts of the data that we want to fetch
        """
        if parts is None:
            parts = MLDL.__PARTS

        with BoundedThreadPoolExecutor(max_workers=self.num_threads) as executor:
            while not self.kill_event.is_set():
                executor.submit(self.filler_worker, num, parts)
            try:
                while not self.responses_queue.empty():
                    self.responses_queue.get()
            except Exception as e:
                print(e)
                pass
            executor.shutdown(wait=True)

    def filler_worker(self, num: int, parts: dict = None):
        if parts is None:
            parts = MLDL.__PARTS
        df = self.fetch_sample(num, parts)
        self.responses_queue.put(df)
        return

    def fetch_sample(self, num: int, parts: dict = None, retry: int = 0):
        """
        This function is used to fetch the data from the database
        Run two threads to fetch the data from the database
        :param num: number of samples
        :param parts: the parts of the data that we want to fetch
        :param retry: number of retries max is constant 7
        :return: dataframe of the data
        """

        if parts is None:
            parts = MLDL.__PARTS
        try:
            # get random row_id from the pool
            index_list = self.requests_queue.get()

            with concurrent.futures.ThreadPoolExecutor() as executor:
                main_thread = executor.submit(self.fetch_sample_main, index_list, parts)
                if parts[MLDL.__INTERACTION] and parts[MLDL.__INTERACTION] == 1:
                    interaction_thread = executor.submit(self.fetch_sample_interaction, index_list)

                main_df = main_thread.result()

                interaction_df = pd.DataFrame()
                if parts[MLDL.__INTERACTION] and parts[MLDL.__INTERACTION] == 1:
                    interaction_df = interaction_thread.result()

                executor.shutdown(wait=True)

                if len(interaction_df) == 0:
                    main_df['interactions'] = np.nan
                    return main_df
                df = pd.merge(main_df, interaction_df, on='row_id', how='left')
                return df
        except Exception as e:
            print(e)
            if retry == 0:
                time.sleep(1)
            else:
                time.sleep(retry * 10)
            retry += 1
            print(f'Cannot fetch data from database, retry number {retry} times')
            if retry > 7:
                raise Exception('Cannot fetch data from database')
            return self.fetch_sample(num, parts, retry)

    def fetch_sample_main(self, index_list: list, parts: dict = None):
        """
        This function is used to fetch the main data from the database
        :param index_list: list of row_ids
        :param parts: parts of the data
        :return: dataframe of main data
        """
        # s = time.perf_counter()
        session = self.Session()
        if parts is None:
            parts = MLDL.__PARTS
        try:
            if self.token_size >= 10 and self.max_length <= 300:
                results = session.query(SeqLang300T10Model).filter(SeqLang300T10Model.row_id.in_(index_list)).all()
            elif self.token_size >= 10:
                results = session.query(SeqLangT10Model).filter(SeqLangT10Model.row_id.in_(index_list)).all()
            elif self.max_length <= 300:
                results = session.query(SeqLang300Model).filter(SeqLang300Model.row_id.in_(index_list)).all()
            else:
                results = session.query(SeqLangModel).filter(SeqLangModel.row_id.in_(index_list)).all()
            session.commit()
            df = pd.DataFrame([r.to_dict() for r in results])
        except Exception as e:
            print(e)
            session.rollback()
            raise Exception('Cannot fetch data from database <SeqLang>')
        finally:
            session.close()
            self.async_flush(session)
        # print('fetch_sample_main')
        # print(time.perf_counter() - s)
        return df

    async def async_flush(self, session):
        await session.flush()

    def fetch_sample_interaction(self, index_list: list):
        """
        This function is used to fetch the interaction data from the database
        :param index_list: list of row_ids
        :return: dataframe of interaction data
        """
        # s = time.perf_counter()
        session = self.Session()
        try:
            if self.token_size >= 10 and self.max_length <= 300:
                results = session.query(Interaction300T10Model).filter(Interaction300T10Model.row_id.in_(index_list)).all()
            elif self.token_size >= 10:
                results = session.query(InteractionT10Model).filter(InteractionT10Model.row_id.in_(index_list)).all()
            elif self.max_length <= 300:
                results = session.query(Interaction300Model).filter(Interaction300Model.row_id.in_(index_list)).all()
            else:
                results = session.query(InteractionModel).filter(InteractionModel.row_id.in_(index_list)).all()
            session.commit()
            df = pd.DataFrame([r.to_dict() for r in results])
        except Exception as e:
            print(e)
            session.rollback()
            raise Exception('Cannot fetch data from database <Interaction>')
        finally:
            session.close()
            self.async_flush(session)
        # print('fetch_sample_interaction')
        # print(time.perf_counter() - s)
        return df

    def fill_request_queue(self, num: int):
        """
        This function is used to fill the queue with requests index from the pool
        :param num:
        :return:
        """
        i = 0
        max_i = len(self.pool) // num
        while not self.kill_fill_requests_event.is_set():
            index_list = self.pool[i * num: (i + 1) * num]
            self.requests_queue.put(index_list)
            i = (i + 1) % max_i

    def terminate(self):
        """
        Terminate the filler threads and clear the queue
        """
        # Terminate the filler thread
        if self.filler_thread is not None:
            self.kill_event.set()
            self.kill_fill_requests_event.set()

            if not self.responses_queue.empty():
                self.responses_queue.get()
            if not self.requests_queue.empty():
                self.requests_queue.get()

            self.filler_thread.join()
            self.fill_request_thread.join()

            self.kill_event.clear()
            self.kill_fill_requests_event.clear()

            self.Session.close_all()
