# -*- coding: utf-8 -*-

# sqlite utils for the project


import sqlite3
import settings as settings
import logging
import sys
import pandas as pd


# 创建一个日志器logger并设置其日志级别为DEBUG
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# 创建一个流处理器handler并设置其日志级别为DEBUG
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

# 创建一个格式器formatter并将其添加到处理器handler
formatter = logging.Formatter(
    "[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s")
handler.setFormatter(formatter)

# 为日志器logger添加上面创建的处理器handler
logger.addHandler(handler)


INSERT_CMD = """INSERT INTO {tbl} (
                    name, url) VALUES ( '{name}', '{url}' );"""
DROP_TABLE_CMD = """DROP TABLE IF EXISTS {tbl};"""
CREATE_TALE_CMD = """CREATE TABLE IF NOT EXISTS {tbl} (
                    id integer primary key,
                    name text,
                    url  text);"""

TEST_INSERT_CMD = """INSERT INTO {tbl} (
                    name, url) VALUES ( '{name}', '{url}' );"""
TEST_CREATE_TALE_CMD = """CREATE TABLE IF NOT EXISTS {tbl} (
                    id integer primary key,
                    name text,
                    url  text);"""


class DataStore(object):
    # utils class

    def __init__(self, reset=False):
        self.db_file_name = settings.SQLITE3_FILE_NAME
        self.db_table_name = settings.SQLITE3_TABLE_NAME
        self.conn = sqlite3.connect(self.db_file_name)
        self.cursor = self.conn.cursor()
        # Delete old records
        if not reset:
            return
        logger.info('Reset table: %s' % (self.db_table_name))
        self.cursor.execute(DROP_TABLE_CMD.format(tbl=self.db_table_name))
        self.cursor.execute(
            TEST_CREATE_TALE_CMD.format(tbl=self.db_table_name))
        self.conn.commit()

    def close(self):
        self.conn.close()

    def save_buddha(self, name, url):
        if '\'' in name:
            name = name.replace('\'', "-")
        if '\'' in url:
            url = url.replace('\'', "-")
        self.cursor.execute(
            TEST_INSERT_CMD.format(tbl=self.db_table_name, name=name, url=url))
        self.conn.commit()

    def fetch_all(self):
        query = "SELECT * FROM {tbl}".format(tbl=self.db_table_name)
        df = pd.read_sql_query(query, self.conn)
        return df

    def fetch_buddha(self, limit=10):
        query = "SELECT * FROM {tbl} LIMIT {limit}".format(
            tbl=self.db_table_name, limit=limit)
        df = pd.read_sql_query(query, self.conn)
        logger.info("\n %s " % (df))
        return df


def main():
    ds = DataStore()
    ds.save_buddha('buddha1', 'http:91')
    logger.info("\n %s " % ds.fetch_buddha())
    ds.close()


if __name__ == '__main__':
    main()
