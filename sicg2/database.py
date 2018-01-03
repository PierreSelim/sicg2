"""Database module for SICG."""

import datetime
import os
import sqlite3
import sys

PY3 = sys.version_info >= (3, )
QUERIES = {
    'createdb': """CREATE TABLE
                IF NOT EXISTS {table} (page_title, views, url, date)""",
    'insert': """INSERT INTO {table}
              VALUES (:page_title, :views, :url, :date)""",
    'list': """SELECT * FROM {table}
            ORDER BY views DESC{limit};""",
    'lastupdate': 'SELECT date FROM {table} ORDER BY date DESC LIMIT 1'
}


class SicgDB(object):

    """Interface with database.

    Used as singleton with SicgDB.get()
    """

    TABLE = 'articles_views'
    __INSTANCE__ = None

    def __init__(self, filename):
        """Contructor.

        Create a new database if not already existing in the sqlite file.

        Args:
            filename (str): filename of the sqlite database file.
        """
        self.connection = sqlite3.connect(filename, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.__create_db__()

    def __create_db__(self):
        """Create a new database if not already existing in the sqlite file."""
        self.cursor.execute('PRAGMA encoding="UTF-8";')
        query = QUERIES['createdb'].format(table=SicgDB.TABLE)
        self.cursor.execute(query)
        self.connection.commit()

    @classmethod
    def get(cls):
        """SicgDB singleton."""
        if not SicgDB.__INSTANCE__:
            db_file = os.environ.get('SICG2_DB', None)
            if not db_file:
                raise ValueError('Need to set SICG2_DB environment variable')
            if not os.path.exists(db_file):
                open(db_file, mode='a').close()
            SicgDB.__INSTANCE__ = cls(db_file)
        return SicgDB.__INSTANCE__

    def insert(self, page_title='', views=None, url=None, date=None):
        """Insert a page in the database."""
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
        """List pages in database ordered by views (with a possible limit)."""
        limit_query = ''
        if limit >= 0:
            limit_query = ' LIMIT %d' % limit
        self.cursor.execute(QUERIES['list'].format(
            limit=limit_query,
            table=SicgDB.TABLE))
        all = self.cursor.fetchall()
        markdown = []
        for article in all:
            article_title = article[0]
            if not PY3:
                article_title = article[0].encode('utf-8')
            markdown.append('* [{title}]({url}) ({views})'.format(
                title=article_title,
                views=article[1],
                url=article[2]
            ))
        return '\n'.join(markdown)

    def lastupdate(self):
        """Most recent date of update in the database."""
        query = QUERIES['lastupdate'].format(table=SicgDB.TABLE)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result:
            result = datetime.datetime \
                             .strptime(result[0], '%Y-%m-%d %H:%M:%S.%f')
        return result
