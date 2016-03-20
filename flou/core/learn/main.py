# main process for learning user preference model.
# overwrites value every time it is run.
import flou.core.learn.db as learn_db
import flou.core.feature.db as feature_db
import flou.user.pred_db as pred_db
import flou.channel.db as feed_db
import flou.user.db as user_db

import json
import time

from flou.core.learn.perceptron import Perceptron
from flou.utils import colorize

EXTRACTION_QUIESCENCE = 300 # seconds between two extractins.
LEARNING_RATE = 1.
NUM_ITER = 100

while True:
    userids = user_db.get_userids()
    for userid in userids:
        print colorize('[learn] user = %s\n' % userid, 'green')

        # model = learn_db.get_model_by_userid(userid)
        model = None

        if not model:
            learner = Perceptron(lr=LEARNING_RATE)
        else:
            learner = Perceptron(lr=LEARNING_RATE,
                                 weight=model['weight'],
                                 G2=model['G2'])

        links = user_db.get_links_by_user(userid)

        # training.
        exs = []
        labels = []
        for link in links:
            action_by_link = user_db.get_actions_by_user(userid)
            for (link, action) in action_by_link.items():
                exs.append(feature_db.get_feature_by_url(link))
                if action == 'like': # like this content.
                    labels.append(1.)
                else: # dislike this content.
                    labels.append(0.)

        for it in range(NUM_ITER):
            learner.train(exs, labels)

        learn_db.save_model_by_userid(userid, learner.to_dict())

        print learner.weight
        # prediction.
        all_entries = feed_db.get_all_entries()
        for entry in all_entries:
            link = entry['link']
            feature = feature_db.get_feature_by_url(link)
            score = learner.score(feature)
            pred_db.add_prediction(userid, link, score)


        print colorize('[sleeping] ~ %s seconds' % EXTRACTION_QUIESCENCE, 'blue')
        time.sleep(EXTRACTION_QUIESCENCE)
