import feedparser
import urllib2
import urllib
import json

import flou.channel.db as db
from flou.utils import colorize
from flou.sanity.readability import extract_reader_html

def fetch(url):
    data = feedparser.parse(url)
    entries = data.get('entries')
    if entries:
        for entry in entries:
            try:
                link = entry.get('link') # fetch link only.
                # use diffbot only to extract contact.
                data = extract_reader_html(link)
                html = data.get('content')
                title = data.get("title")
                cover = data.get("cover")
                db.add_entry(link, title, kind='article', data=json.dumps(data))
                print colorize('[rss extracted] [source: %s] %s' % (url, link), 'green')
            except Exception as e:
                print '[error] extract link failed', link, e.message


if __name__ == '__main__':
    fetch('http://hnrss.org/newest')


