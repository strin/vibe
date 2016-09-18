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
        conn.execute("""CREATE TABLE IF NOT EXISTS predict
                    (userid text,
                     link text,
                     prediction REAL)
                    """)
        conn.commit()
        self.conn = conn
        return conn

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()


def get_by_user_link(userid, link):
    with DBConn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT * FROM predict WHERE userid=:userid AND link=:link
                       """, dict(link=link, userid=userid))
        row = cursor.fetchone()
        return row


def add_prediction(userid, link, prediction):
    with DBConn() as conn:
        cursor = conn.cursor()
        if get_by_user_link(userid, link): # response exists in DB
            cursor.execute("""
                    UPDATE predict
                    SET prediction=:prediction
                    WHERE
                        userid=:userid
                    AND
                        link=:link
                    """,
                    dict(userid=userid,
                         link=link,
                         prediction=prediction)
                    )
        else:
            cursor.execute("""
                    INSERT INTO predict
                        (userid,
                        link,
                        prediction)
                    VALUES
                       (:userid,
                       :link,
                       :prediction)
                    """,
                    dict(userid=userid,
                         link=link,
                         prediction=prediction)
                    )


def get_links_sorted(userid):
    '''
    get unread content sorted by score.
    '''
    with DBConn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT link FROM predict WHERE userid=:userid
                       ORDER BY prediction DESC
                       """, dict(userid=userid))
        rows = cursor.fetchall()
        if rows:
            links = [row['link'] for row in rows]
            return links
        else:
            return []


def get_link_pred_sorted(userid):
    '''
    get (link, prediction) pairs
    '''
    with DBConn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT link, prediction FROM predict WHERE userid=:userid
                       ORDER BY prediction DESC
                       """, dict(userid=userid))
        rows = cursor.fetchall()
        if rows:
            return [(row['link'], row['prediction']) for row in rows]
        else:
            return []
