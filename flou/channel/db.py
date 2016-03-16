import sqlite3 as sql
import base64
import json

from flou.utils import mkdir_if_not_exists
from flou.db.common import DB_FILE_NAME, DB_PATH_NAME

class DBConn(object):
    def __enter__(self):
        conn = sql.connect(DB_FILE_NAME)
        conn.row_factory = sql.Row
        # create the file metadata table.
        # type: image, video, album, ...
        # data:
        #   image: url
        #   mp4:   url
        #   album: list of json objects.
        conn.execute("""CREATE TABLE IF NOT EXISTS feed
                    (title text,
                    link text,
                    type text,
                    data text)
                    """)
        conn.commit()
        self.conn = conn
        return conn

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()

def get_by_url(link):
    '''
    >>> get_by_url('https://github.com/samyk/magspoof')['title']
    u'MagsProof'
    '''
    with DBConn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT * FROM feed WHERE link=:link
                       """, dict(link=link))
        row = cursor.fetchone()
        return row
    return None



def get_all_entries():
    with DBConn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT * FROM feed
                       """)
        rows = cursor.fetchall()
        return rows
    return None


def add_entry(link, title, kind, data):
    '''
    >>> add_entry('https://github.com/samyk/magspoof', 'MagsProof', 'MagSpoof - credit card/magstripe spoofer')
    '''
    if get_by_url(link): # link exists in DB
        return

    with DBConn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                    INSERT INTO feed
                        (title,
                        link,
                        type,
                        data)
                    VALUES
                       (:title,
                       :link,
                       :type,
                       :data)
                    """,
                    dict(title=title,
                         link=link,
                         type=kind,
                         data=data)
                    )

if __name__ == '__main__':
    import doctest
    doctest.testmod()
