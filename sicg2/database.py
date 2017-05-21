import datetime
import os
import sqlite3


QUERIES = {
    'createdb': """CREATE TABLE
                IF NOT EXISTS {table} (page_title, views, url, date)""",
    'insert': """INSERT INTO {table}
              VALUES (:page_title, :views, :url, :date)""",
    'list': """SELECT * FROM {table}
            ORDER BY views DESC{limit};"""
}


class SicgDB(object):

    TABLE = 'articles_views'
    __INSTANCE__ = None

    def __init__(self, filename):
        self.connection = sqlite3.connect(filename, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.__create_db__()

    def __create_db__(self):
        self.cursor.execute('PRAGMA encoding="UTF-8";')
        query = QUERIES['createdb'].format(table=SicgDB.TABLE)
        self.cursor.execute(query)
        self.connection.commit()

    @classmethod
    def get(cls):
        if not SicgDB.__INSTANCE__:
            db_file = os.environ.get('SICG2_DB', None)
            if not db_file:
                raise ValueError('Need to set SICG2_DB environment variable')
            SicgDB.__INSTANCE__ = cls(db_file)
        return SicgDB.__INSTANCE__


    def insert(self, page_title='', views=None, url=None, date=None):
        query = QUERIES['insert'].format(table=SicgDB.TABLE)
        last_update = date or datetime.datetime.now()
        self.cursor.execute(query, {
            'page_title': page_title,
            'views': views,
            'url': url,
            'date': last_update
        })
        self.connection.commit()

    def list(self, limit=None):
        limit_query = ''
        if limit >= 0:
            limit_query = ' LIMIT %d' % limit
        self.cursor.execute(QUERIES['list'].format(
            limit=limit_query,
            table=SicgDB.TABLE))
        all = self.cursor.fetchall()
        markdown = []
        for article in all:
            markdown.append('* [{title}]({url}) ({views})'.format(
                title=article[0].encode('utf-8'),
                views=article[1],
                url=article[2]
            ))
        return '\n'.join(markdown)