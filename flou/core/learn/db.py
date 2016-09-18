import sqlite3 as sql
import json
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
        conn.execute("""CREATE TABLE IF NOT EXISTS model
                    (userid text PRIMARY KEY,
                     model text
                    )
                    """)
        conn.commit()
        self.conn = conn
        return conn

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()


def get_model_by_userid(userid):
    with DBConn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT * FROM model WHERE userid=:userid
                       """, dict(userid=userid))
        row = cursor.fetchone()
        if row:
            row = dict(row)
            return json.loads(row['model'])
    return {}


def save_model_by_userid(userid, model):
    with DBConn() as conn:
        cursor = conn.cursor()
        if get_model_by_userid(userid):
            cursor.execute("""
                            UPDATE model
                            SET model=:model
                            WHERE
                                userid=:userid
                            """,
                            dict(userid=userid,
                                model=json.dumps(model)
                            )
                        )
        else:
            cursor.execute("""
                            INSERT INTO model
                                (userid,
                                model
                                )
                            VALUES
                            (:userid,
                            :model)
                            """,
                            dict(userid=userid,
                                model=json.dumps(model)
                            )
                        )
