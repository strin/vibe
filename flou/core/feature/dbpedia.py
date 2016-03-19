import urllib2
import urllib
import json
import traceback
import csv
import re
import feedparser
from pprint import pprint
# feature extraction given dbpedia keyword,

class DBpedia(object):
    def __init__(self, word):
        self.category = []
        self.type = []
        try:
            data = feedparser.parse('http://dbpedia.org/data/%s.atom' % word)
            for link in data['entries'][0]['links']:
                rel = link['rel']
                href = link['href']
                if rel == 'http://purl.org/dc/terms/subject':
                    self.category.extend(
                        re.findall(r'http://dbpedia.org/resource/Category:(.*)', href)
                    )
                elif rel == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
                    self.type.extend(
                        re.findall(r'http://dbpedia.org/ontology/(.*)', href)
                    )
        except Exception as e:
            print '[DPpedia error] cannot extract word %s' % word, e.message
            traceback.print_exc()


def feat_dbpedia(link, whitelist):
    ''' given a dbpedia link, such as http://dbpedia.org/resource/Loyalty,
    extract its categories '''
    word = re.findall(r'http://dbpedia.org/resource/(.*)', link)
    feat = {}
    if not word:
        return feat
    word = word[0]
    for key in whitelist:
        db = DBpedia(word)
        if getattr(db, key):
            objs = getattr(db, key)
            for obj in objs:
                feat[key + '-' + obj] = 1.
    return feat


def feat_dbpedia_all(link):
    return feat_dbpedia(link, ['category', 'type'])


