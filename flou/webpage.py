import urllib
import json
from bs4 import BeautifulSoup

def __parse_readability(url):
    raw_data =  urllib.urlopen('http://www.readability.com/api/content/v1/parser?url=%(url)s&token=60082179dbe5bc0e7a7d38b8478ea9e90298cd1a' %
                           dict(url=url)).read()
    data = json.loads(raw_data)
    return {
        'content': data['content'],
        'word_count': data['word_count']
    }

def __extract_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()

def extract_text(url):
    '''
    >>> len(extract_text('https://github.com/samyk/magspoof')) > 0
    True
    '''
    html = __parse_readability(url)['content']
    return __extract_text(html)

if __name__ == '__main__':
    import doctest
    doctest.testmod()


