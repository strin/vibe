# main process for learning user preference model.
from flou.core.learn.db import get_model_by_userid, save_model_by_userid
import flou.core.feature.db as feature_db

from flou.utils import colorize

EXTRACTION_QUIESCENCE = 300 # seconds between two extractins.
