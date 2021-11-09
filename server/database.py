'''
    A class with the specific intent of making
    database actions easy & decluttered.

    Verified: 2021 February 7
    * Follows PEP8
    * Tested Platforms
        * Windows 10
'''

from server.state import ServerStatic

import sqlite3
import os


class Database:

    __DATABASE_FN = 'database.db'

    def __init__(self):
        if not os.path.isdir(ServerStatic.ARCHIVE_DIR):
            os.makedirs(ServerStatic.ARCHIVE_DIR, exist_ok=True)

        self.__conn = sqlite3.connect(os.path.join(
                                      ServerStatic.ARCHIVE_DIR,
                                      Database.__DATABASE_FN))
        self.__cursor = self.__conn.cursor()

    def commit(self):
        self.__conn.commit()

    def close(self):
        self.__conn.close()

    def execute(self, sql, values=()):
        self.__cursor.execute(sql, values)

    def create_table(self, table, **kwargs):
        self.__cursor.execute(
            'CREATE TABLE IF NOT EXISTS '
            '{} ({}, UNIQUE ({}) ON CONFLICT IGNORE)'.format(
                table, Database.parse(kwargs), ','.join(kwargs)))

    def read(self, table, fields=('*',), fetch=0, condition=()):
        self.__cursor.execute('SELECT {} FROM {}{}'.format(
            ','.join(fields), table, (' WHERE {}{}?'.format(
                *condition[:2]) if condition else '')
            ), (condition[2],) if condition else condition)

        if fetch > 0:
            return self.__cursor.fetchmany(fetch)
        else:
            return self.__cursor.fetchall()

    def write(self, table, values):
        self.__cursor.execute('INSERT INTO {} VALUES ({})'.format(
            table, ','.join(tuple('?' * len(values)))), values)

    def update(self, table, condition, **kwargs):
        self.__cursor.execute('UPDATE {} SET {} WHERE {}{}?'.format(
            table, Database.parse({
                key: '?' for key in kwargs
            }, '='), *condition[:2]
        ), list(kwargs.values()) + [condition[2]])

    def delete(self, table, condition):
        self.__cursor.execute('DELETE FROM {} WHERE {}{}?'.format(
            table, *condition[:2]), (condition[2],))

    @staticmethod
    def parse(dictionary, seperator=' '):
        return ','.join((key + seperator + value
                        for key, value in dictionary.items()))
