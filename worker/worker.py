import json
import time
from codecs import open
import boto3
from alchemyapi import AlchemyAPI
from create import create_topic

alchemyapi = AlchemyAPI()

sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='TwittMap')
topic = create_topic()


def appendlog(f, s):
    f.write(u'[{0}] {1}\n'.format(time.strftime('%Y-%m-%dT%H:%M:%SZ'), s))
    f.flush()


if __name__ == '__main__':
    with open('worker.log', 'a', encoding='utf8') as f:
        appendlog(f, 'Program starts')
        while True:
            for message in queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=20):
                try:
                    tweet = json.loads(message.body)
                    response = alchemyapi.sentiment('text', tweet['text'])
                    if response['status'] == 'OK':
                        tweet['sentiment'] = response['docSentiment']['type']
                        encoded = json.dumps(tweet, ensure_ascii=False)
                        # Push to Amazon SNS
                        topic.publish(Message=encoded)
                        appendlog(f, '{0}: {1}'.format(tweet['sentiment'], tweet['text']))
                    else:
                        appendlog(f, 'Analysis failed: {0}'.format(tweet['text']))
                except Exception as e:
                    appendlog(f, '{0}: {1}'.format(type(e), str(e)))
                finally:
                    message.delete()
