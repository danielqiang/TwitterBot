import tweepy


# Enter your consumer key/access token pairs.
CONSUMER_KEY = ''
CONSUMER_KEY_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

# Handle Twitter OAuth
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# If Twitter refuses a tweepy request due to rate limit, wait
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def parse(text):
    """
    Parses text for a twitter status and returns relevant "action" keywords.
    """
    twitter_actions = ['follow', 'retweet', 'rt', 'comment', 'like', 'fav']
    return [action for action in twitter_actions if action in text]


def perform_twitter_action(action, tweet_handle):
    """
    Given a list of twitter "action" keywords and a tweet handle (id),
    perform the specified action on the tweet handle.
    Example: perform_twitter_action("retweet", tweet_handle)
    -> Retweet the tweet specified by the tweet handle object

    :type action: string
    :type tweet_handle: tweepy Status object.
    :return:
    """
    if action in ['retweet', 'rt']:
        api.retweet(tweet_handle.id)
    elif action in ['like', 'fav']:
        api.create_favorite(tweet_handle.id)
    elif action == 'follow':
        if 'retweeted_status' in tweet_handle._json:
            api.create_friendship(tweet_handle._json['retweeted_status']['user']['id'])
        else:
            api.create_friendship(tweet_handle._json['user']['id'])
    elif action == 'comment':
        api.update_status('Hmu please, I really want it', in_reply_to_status_id=tweet_handle.id)


def clear():
    for user_id in api.friends_ids():
        api.destroy_friendship(user_id)
    for i, tweet_handle in enumerate(tweepy.Cursor(api.home_timeline).items()):
        api.destroy_status(tweet_handle.id)


def main():
    results = tweepy.Cursor(api.search, q="chance to win").items(1000)
    for i, result in enumerate(results):
        # If there are twitter actions to perform, it's likely an contest
        actions = parse(result.text.lower())
        if actions:
            for action in actions:
                try:
                    perform_twitter_action(action, result)
                except tweepy.error.TweepError:
                    pass


if __name__ == '__main__':
    while True:
        main()
