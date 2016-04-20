
import urllib2
import urllib
import json

def extract_reader_html(url):
    response = urllib2.urlopen('http://api.diffbot.com/v3/article?%s'
                        % urllib.urlencode({
                            'token': '75cfd1a36dcbb3eb786fcb7111113a37',
                            'url': url
                        }))
    data = json.load(response)['objects'][0]
    images = data.get('images')
    image = ''
    if images:
        for potential_im in images:  # extract image based on diffbot's visual analysis.
            if 'primary' in potential_im and potential_im['primary']:
                image = potential_im['url']
        if not image: # if visual analysis fails, then use defifinition of image.
            # sort images based on resolution.
            try:
                images = sorted(images,
                                key=lambda image: image['width'] * image['height'],
                                reverse=True)
            except:
                pass
            image = images[0]['url']

    return {
        'content': data.get('html'),
        'title': data.get('title'),
        'date': data.get('estimatedDate'),
        'author': data.get('author'),
        'cover': image,
        'tags': data.get('tags')
    }


