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
        conn.execute("""CREATE TABLE IF NOT EXISTS feature
                    (link text PRIMARY KEY,
                     feature text
                    )
                    """)
        conn.commit()
        self.conn = conn
        return conn

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()


def get_feature_by_url(link):
    with DBConn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT * FROM feature WHERE link=:link
                       """, dict(link=link))
        row = cursor.fetchone()
        if row:
            row = dict(row)
            if 'feature' in row:
                row['feature'] = json.loads(row['feature'])
        return row
    return None


def save_feature_by_url(link, feature):
    with DBConn() as conn:
        cursor = conn.cursor()
        if get_feature_by_url(link):
            cursor.execute("""
                            UPDATE feature
                            SET feature=:feature
                            WHERE
                                link=:link
                            """,
                            dict(link=link,
                                feature=json.dumps(feature)
                            )
                        )
        else:
            cursor.execute("""
                            INSERT INTO feature
                                (link,
                                feature
                                )
                            VALUES
                            (:link,
                            :feature)
                            """,
                            dict(link=link,
                                feature=json.dumps(feature)
                            )
                        )

