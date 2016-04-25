import json
import boto3
from alchemyapi import AlchemyAPI
from create import create_topic
from multiprocessing import Pool

alchemyapi = AlchemyAPI()

sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='TwittMap')
topic = create_topic()


def worker(_):
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
            finally:
                message.delete()


if __name__ == '__main__':
    pool = Pool(3)
    pool.map(worker, range(3))
