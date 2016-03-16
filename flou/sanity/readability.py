import urllib2
import urllib
import json


def extract_reader_html(url):
    response = urllib2.urlopen('''https://www.readability.com/api/content/v1/parser?%s'''
                        % urllib.urlencode({
                            'url': url,
                            'token': 'bce960b8684303b648a519238bb7f6ff3c1d1ddc'
                        }))
    content = json.load(response)['content']
    content = content.replace('\n', '') # remove unnecessary newlines
    return content


