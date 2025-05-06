import psycopg2
from psycopg2 import sql
import os
import logging
from contextlib import contextmanager

context_logger = '[Neon DB - connection]'
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("config")

class DBPool:
    def __init__(self, connection_string, max_connections=5):
        self.connection_string = connection_string
        self.max_connections = max_connections
        self.pool = None 

    def get_connection(self):
        return psycopg2.connect(self.connection_string)

db_pool = DBPool(os.getenv('DATABASE_URL', 'postgresql://neondb_owner:npg_BlhGFJT9I3tj@ep-empty-haze-a1aif6rd-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'))


def db_connection():
    try:
        conn = db_pool.get_connection()
        with conn.cursor() as cursor:
            cursor.execute('SELECT 1')
            cursor.execute('SELECT version()')
            version = cursor.fetchone()
            logger.info(f'{context_logger} | Database connection successfully')
            logger.info(f'{context_logger} | version: {version[0]}')
        conn.close()
    except Exception as err:
        logger.error(f'{context_logger} | Database connection error', exc_info=True)
        raise err


def command_with_params(sql_query, params=None):
    if params is None:
        params = []
    conn = db_pool.get_connection()
    try:
        with conn.cursor() as cursor:
            logger.info(f'{context_logger} | Info - SQL: {sql_query} - Params: {params}')
            cursor.execute(sql_query, params)
            result = cursor.fetchall()
            return result
    except Exception as err:
        logger.error(f'{context_logger} | Database query error', exc_info=True)
        raise err
    finally:
        conn.close()


def execute_sql_query(sql_query, params=None):
    return command_with_params(sql_query, params)


@contextmanager
def start_transaction():
    conn = db_pool.get_connection()
    try:
        with conn.cursor() as cursor:
            logger.info(f'{context_logger} | Info | transaction')
            cursor.execute('BEGIN')
            yield cursor
        conn.commit()
    except Exception as err:
        logger.error(f'{context_logger} | Transaction error', exc_info=True)
        conn.rollback()
        raise err
    finally:
        conn.close()


def execute_sql_transaction(cursor, sql_query, params=None):
    if params is None:
        params = []
    try:
        logger.info(f'{context_logger} | Info - SQL: {sql_query} - Params: {params}')
        cursor.execute(sql_query, params)
        return cursor.fetchall()
    except Exception as err:
        logger.error(f'{context_logger} | Transaction query error', exc_info=True)
        raise err


def rollback_transaction(cursor):
    try:
        cursor.connection.rollback()
    except Exception as err:
        logger.error(f'{context_logger} | Rollback error', exc_info=True)
        raise err


def commit_transaction(cursor):
    try:
        cursor.connection.commit()
    except Exception as err:
        logger.error(f'{context_logger} | Commit error', exc_info=True)
        raise err
