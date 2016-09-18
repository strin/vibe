# main backfill process for feature extraction
# does not overwrite value every time it is run.
import flou.channel.db as channel_db
import flou.core.feature.db as feature_db

import json
import time

from flou.core.feature.dbpedia import feat_dbpedia_all
from flou.utils import colorize

EXTRACTION_QUIESCENCE = 300 # seconds between two extractins.

while True:
    items = channel_db.get_all_entries()
    for item in items:
        data = json.loads(item['data'])
        link = item['link']
        if feature_db.get_feature_by_url(link): # do not extract ones that exist.
            print colorize('[skipping] %s\n' % (link), 'red')
            continue
        tags = data.get('tags')
        feature = {}
        if tags:
            for tag in tags:
                tag_feat = feat_dbpedia_all(tag['uri'])
                # normalize feature by relevance score.
                tag_feat = {key: val * tag['score'] for (key, val) in tag_feat.items()}
                # add to feature pool.
                feature.update(tag_feat)

        print colorize('[extracted] %s\n%s\n\n' % (link, json.dumps(feature)), 'green')
        feature_db.save_feature_by_url(link, feature)

    print colorize('[sleeping] ~ %s seconds' % EXTRACTION_QUIESCENCE, 'blue')
    time.sleep(EXTRACTION_QUIESCENCE)


