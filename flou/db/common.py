from flou.utils import mkdir_if_not_exists

DB_FILE_NAME = 'flou/db/feed.db'
DB_PATH_NAME = DB_FILE_NAME[:DB_FILE_NAME.rfind('/')]

mkdir_if_not_exists(DB_PATH_NAME)

