''' Extracts news from arxiv.org
The code uses arxiv API:
    http://arxiv.org/help/api/index
also references implementation of arxiv-sanity preserver
    https://github.com/karpathy/arxiv-sanity-preserver/
'''
from __future__ import print_function
from pprint import pprint
import feedparser
import requests
import traceback
import json

import flou.channel.db as db
from flou.utils import colorize
import dateparser

DEFAULT_CATEGORY = 'cat:cs.CV+OR+cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL+OR+cat:cs.NE+OR+cat:stat.ML'
API_URL = 'http://export.arxiv.org/api/query'

def clean_abstract(abstract):
    abstract = abstract.replace('\n', ' ')
    return abstract

def clean_title(title):
    # TODO: this is a hack to deal with titles like
    # Accurate De Novo Prediction of Protein Contact Map by Ultra-Deep\n  Learning Model
    title = title.replace('\n  ', ' ')
    return title

def fetch(max_count=30, category=DEFAULT_CATEGORY):
    query = ('search_query=%(query)s&'
             'sortBy=lastUpdatedDate&'
             'start=0&max_results=%(max_count)i' %
             dict(query=category,
                  max_count=max_count))
    response = requests.get(API_URL + '?' + query).content
    result = feedparser.parse(response)
    if result.entries:
        try:
            for e in result.entries:
                link = e['link']
                title = clean_title(e['title'])
                abstract = clean_abstract(e['summary'])
                date = dateparser.parse(e['updated'])
                data = {
                    'link': link,
                    'title': title,
                    'date': date.isoformat(),
                    'authors': e['authors'],
                    'abstract': abstract
                }
                print(data)
                db.add_entry(link, title, date, kind='paper', data=json.dumps(data))
                print(colorize('[channel arixv] %s' % link, 'blue'))
        except Exception as e:
            print(colorize('[channel arixv][error] %s' % link), 'red')
            print(e.message)
            traceback.print_exc(file=sys.stdout)


if __name__ == '__main__':
    fetch()
