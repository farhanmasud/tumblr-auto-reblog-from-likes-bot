CONSUMER_KEY = ""
CONSUMER_SECRET = ""
OAUTH_TOKEN = ""
OAUTH_SECRET = ""

# example
# BLOG_NAME = "myblog.tumblr.com"
BLOG_NAME = ""

LIMIT = 50

TIMESTAMP_FILE = "last_timestamp.txt"

try:
    from .local_settings import *
except ImportError:
    pass
