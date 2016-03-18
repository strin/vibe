from tornado import (ioloop, web)

import flou.channel.db as db
import flou.channel.rss as rss
import flou.channel.imgur as imgur

import flou.user.db as user_db

from multiprocessing import Process
import time
import json


def fetch_process_method():
    while True:
        # fetch hacker news.
        urls = ['http://hnrss.org/newest',
                'http://www.kurzweilai.net/feed',
                'https://news.google.com/news?pz=1&cf=all&ned=us&hl=en&topic=h&num=3&output=rss',
                'http://www.engadget.com/rss-full.xml',
                'http://rss.sciam.com/ScientificAmerican-Global',
                'http://www.theverge.com/rss/full.xml',
                'http://www.technologyreview.com/rss/rss.aspx',
                'http://feeds.newscientist.com/science-news',
                'http://venturebeat.com/category/cloud/feed/']
        rss.fetch(url, max_count=max_count)
        time.sleep(3600)


fetch_process = Process(target=fetch_process_method)
fetch_process.start()


class FeedHandler(web.RequestHandler):
    def get(self):
        '''
        return all feeds in the database that have images.
        '''
        print '[feed] get feed content'
        userid = self.get_argument('userid')
        print '[feed] userid', userid
        user_links = user_db.get_links_by_user(userid)
        user_links = set(user_links)
        print '[feed] user_links', user_links

        self.set_header("Access-Control-Allow-Origin", "http://localhost:8100")
        entries = db.get_all_entries()
        feeds = []
        for entry in entries:
            feed = dict(entry)
            link = feed.get('link')
            if link and link not in user_links: # user hasn't read this yet.
                feeds.append(feed)

        self.write({
            'feed': feeds
        })


class SwipeHandler(web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        userid = data.get('userid')
        link = data.get('link')
        action = data.get('action')
        print 'link', link
        user_db.add_entry(userid, link, action)
        self.write({
            'status': 'OK'
        })



handlers = [
    # try
    (r"/(.*\.jpg)", web.StaticFileHandler, {"path": "frontend/"}),
    (r"/(.*\.png)", web.StaticFileHandler, {"path": "frontend/"}),
    (r"/(.*\.css)", web.StaticFileHandler, {"path": "frontend/css/"}),
    (r"/(.*\.js)", web.StaticFileHandler, {"path": "frontend/js/"}),
    (r"/vibes/?", FeedHandler),
    (r"/swipe/?", SwipeHandler),
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

