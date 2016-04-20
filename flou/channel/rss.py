import feedparser
import urllib2
import urllib
import json

import flou.channel.db as db
from flou.utils import colorize
# from flou.sanity.readability import extract_reader_html
from flou.sanity.diffbot import extract_reader_html

def fetch(url, max_count=30):
    data = feedparser.parse(url)
    entries = data.get('entries')
    if entries:
        for (count, entry) in enumerate(entries):
            if count >= max_count:
                break
            try:
                link = entry.get('link') # fetch link only.
                print colorize('[rss link] [source: %s] %s' % (url, link), 'blue')
                if db.get_by_url(link): # skip extraction if url exists in db. save extractor quota.
                  continue
                import pdb; pdb.set_trace()
                # use diffbot only to extract contact.
                data = extract_reader_html(link)
                html = data.get('content')
                title = data.get("title")
                cover = data.get("cover")
                if not cover:
                    continue
                db.add_entry(link, title, kind='article', data=json.dumps(data))
            except Exception as e:
                print colorize('[rss extraction] [source: %s] %s' % (url, link), 'green')
                print '[error] extract link failed', link, e.message
                raise e


if __name__ == '__main__':
    fetch('http://hnrss.org/newest')


