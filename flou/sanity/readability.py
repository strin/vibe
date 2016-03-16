import urllib2
import urllib
import json


def extract_reader_html(url):
    response = urllib2.urlopen('''https://www.readability.com/api/content/v1/parser?%s'''
                        % urllib.urlencode({
                            'url': url,
                            'token': 'bce960b8684303b648a519238bb7f6ff3c1d1ddc'
                        }))
    data = json.load(response)
    data['content'] = data['content'].replace('\n', '') # remove unnecessary newlines
    return {
        'content': data.get('content'),
        'title': data.get('title'),
        'cover': data.get('lead_image_url')
    }


