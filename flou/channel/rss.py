import feedparser
import urllib2
import urllib
import json

import flou.channel.db as db

def fetch(url):
    data = feedparser.parse(url)
    entries = data.get('entries')
    if entries:
        for entry in entries:
            try:
                link = entry.get('link') # fetch link only.
                # use diffbot only to extract contact.
                response = urllib2.urlopen('http://api.diffbot.com/v3/article?%s'
                                    % urllib.urlencode({
                                        'token': '0e14244dd75533a5211f1e6b3baf75de',
                                        'url': link
                                    }))
                content = json.load(response)

                main_object = content['objects'][0]
                title = main_object.get("title")
                images = main_object.get("images")
                if images and len(images) > 0:
                    # sort images based on resolution.
                    try:
                        images = sorted(images,
                                        key=lambda image: image['width'] * image['height'],
                                        reverse=True)
                    except:
                        pass
                    image = images[0]['url']
                else:
                    image = ''
                html = main_object.get('html')
                print 'title', title
                print 'url', url
                print 'image', image
                db.add_entry(link, title, image, html)
            except Exception as e:
                print '[error] extract link failed', link, e.message


if __name__ == '__main__':
    fetch('http://hnrss.org/newest')


