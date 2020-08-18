import pytumblr

from configs import CONSUMER_KEY, CONSUMER_SECRET, OAUTH_SECRET, OAUTH_TOKEN

client = pytumblr.TumblrRestClient(
    CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_SECRET
)

print(client.info())
