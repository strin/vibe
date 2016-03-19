''' main backfill process for feature extraction '''
import flou.channel.db as channel_db
import flou.core.feature.db as feature_db

import json

from flou.core.feature.dbpedia import feat_dbpedia_all

EXTRACTION_QUIESCENCE = 300 # seconds between two extractins.

while True:
    items = channel_db.get_all_entries()
    for item in items:
        data = json.loads(item['data'])
        link = item['link']
        tags = data.get('tags')
        feature = {}
        if tags:
            for tag in tags:
                tag_feat = feat_dbpedia_all(tag['uri'])
                # normalize feature by relevance score.
                tag_feat = {key: val * tag['score'] for (key, val) in tag_feat.items()}
                # add to feature pool.
                feature.update(tag_feat)

        print feature
        feature_db.save_feature_by_url(link, feature)




