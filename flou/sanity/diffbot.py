
import urllib2
import urllib
import json

def extract_reader_html(url):
    response = urllib2.urlopen('http://api.diffbot.com/v3/article?%s'
                        % urllib.urlencode({
                            'token': '0e14244dd75533a5211f1e6b3baf75de',
                            'url': url
                        }))
    content = json.load(response)
    return content


