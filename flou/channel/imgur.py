from imgurpython import ImgurClient

import flou.channel.db as db
from flou.utils import colorize
from flou.sanity.readability import extract_reader_html

CLIENT_ID = '19cf41be9c6e96a'
CLIENT_SECRET = 'a4e40ee2d5383632c96aa62d672b06f39a8011ce'

client = ImgurClient(CLIENT_ID, CLIENT_SECRET)

def fetch():
    items = client.gallery(section='hot', sort='viral', page=0, window='day', show_viral=True)
    if items:
        for item in items:
            try:
                link = item.link
                title = item.title
                if item.is_album:
                    html = extract_reader_html(link)
                    image = 'http://i.imgur.com/%s.jpg' % item.cover
                else:
                    html = ''
                    image = link
                db.add_entry(link, title, image, html)
                print colorize('[imgur extracted] %s' % link, 'green')
            except Exception as e:
                print '[error] extract link failed', link, e.message

