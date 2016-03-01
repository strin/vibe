from tornado import (ioloop, web)

import flou.channel.db as db
import flou.channel.rss as rss

from multiprocessing import Process
import time


def fetch_process_method():
    while True:
        url = 'http://hnrss.org/newest'
        print '[fetch]', url
        rss.fetch(url)
        time.sleep(3600)


fetch_process = Process(target=fetch_process_method)
fetch_process.start()


class FeedHandler(web.RequestHandler):
    def get(self):
        '''
        return all feeds in the database that have images.
        '''
        self.set_header("Access-Control-Allow-Origin", "http://localhost:8889")
        entries = db.get_all_entries()
        feeds = []
        for entry in entries:
            feed = dict(entry)
            feeds.append(feed)

        self.write({
            'feed': feeds
        })


handlers = [
    # try
    (r"/(.*\.jpg)", web.StaticFileHandler, {"path": "frontend/"}),
    (r"/(.*\.png)", web.StaticFileHandler, {"path": "frontend/"}),
    (r"/(.*\.css)", web.StaticFileHandler, {"path": "frontend/css/"}),
    (r"/(.*\.js)", web.StaticFileHandler, {"path": "frontend/js/"}),
    (r"/", FeedHandler),
]

settings = {
    "autoreload": True,
    "debug": True,
    "template_path": "."
}

if __name__ == "__main__":
    application = web.Application(handlers, **settings)
    application.listen(8889, address="0.0.0.0")
    ioloop.IOLoop.current().start()

