import json
import time
from codecs import open
from dateutil import parser
import tweepy
import boto3
from tokens import consumer_key, consumer_secret, access_token, access_token_secret

sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='TwittMap')


def appendlog(f, s):
    f.write(u'[{0}] {1}\n'.format(time.strftime('%Y-%m-%dT%H:%M:%SZ'), s))
    f.flush()


class TwittMapListener(tweepy.StreamListener):
    def __init__(self, f):
        super(TwittMapListener, self).__init__()
        self.f = f

    def on_data(self, data):
        try:
            # Reference: https://dev.twitter.com/overview/api/tweets
            decoded = json.loads(data)
            if decoded.get('lang') == 'en' and decoded.get('coordinates') is not None:
                geo = decoded['coordinates']['coordinates']
                timestamp = parser.parse(decoded['created_at']).strftime('%Y-%m-%dT%H:%M:%SZ')
                tweet = {
                    'user': decoded['user']['screen_name'],
                    'text': decoded['text'],
                    'geo': geo,
                    'time': timestamp
                }
                encoded = json.dumps(tweet, ensure_ascii=False)
                queue.send_message(MessageBody=encoded)
                appendlog(self.f, encoded)
        except Exception as e:
            appendlog(self.f, '{0}: {1}'.format(type(e), str(e)))

    def on_error(self, status):
        if status == 420:  # rate limited
            appendlog(self.f, 'Error 420')
            return False


if __name__ == '__main__':
    with open('streaming.log', 'a', encoding='utf8') as f:
        appendlog(f, 'Program starts')

        ls = TwittMapListener(f)
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = tweepy.Stream(auth, ls)
        stream.filter(track=["Trump", "Hillary", "Sanders", "Facebook", "LinkedIn",
                             "Amazon", "Google", "Uber", "Columbia", "New York"])
