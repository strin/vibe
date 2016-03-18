
import urllib2
import urllib
import json

def extract_reader_html(url):
    response = urllib2.urlopen('http://api.diffbot.com/v3/article?%s'
                        % urllib.urlencode({
                            'token': '006799de5f2050af55268df703a73840',
                            'url': url
                        }))
    data = json.load(response)
    images = data.get("images")
    image = ''
    if images:
        for potential_im in images:  # extract image based on diffbot's visual analysis.
            if potential_im['primary']:
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
        'date': data.get('date'),
        'author': data.get('author'),
        'cover': image,
        'tags': data.get('tags')
    }


