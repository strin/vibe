# database utils for storing user behaviors.
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
        conn.execute("""CREATE TABLE IF NOT EXISTS swipe
                    (userid text,
                     link text,
                    action text)
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
                       SELECT * FROM swipe WHERE userid=:userid AND link=:link
                       """, dict(link=link, userid=userid))
        row = cursor.fetchone()
        return row


def get_links_by_user(userid):
    with DBConn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT link FROM swipe WHERE userid=:userid
                       """, dict(userid=userid))
        rows = cursor.fetchall()
        if rows:
            links = [row['link'] for row in rows]
            return links
        else:
            return []


def get_actions_by_user(userid):
    with DBConn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT link, action FROM swipe WHERE userid=:userid
                       """, dict(userid=userid))
        rows = cursor.fetchall()
        action_by_link = {}
        if rows:
            action_by_link = {
                row['link']: row['action'] for row in rows
            }
        return action_by_link


def get_userids():
    with DBConn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT DISTINCT userid FROM swipe
                       """)
        rows = cursor.fetchall()
        if rows:
            userids = [row['userid'] for row in rows]
            return userids
        else:
            return []


def add_entry(userid, link, action):
    with DBConn() as conn:
        cursor = conn.cursor()
        if get_by_user_link(userid, link): # response exists in DB
            cursor.execute("""
                    UPDATE swipe
                    SET action=:action
                    WHERE
                        userid=:userid
                    AND
                        link=:link
                    """,
                    dict(userid=userid,
                         link=link,
                         action=action)
                    )
        else:
            cursor.execute("""
                    INSERT INTO swipe
                        (userid,
                        link,
                        action)
                    VALUES
                       (:userid,
                       :link,
                       :action)
                    """,
                    dict(userid=userid,
                         link=link,
                         action=action)
                    )



