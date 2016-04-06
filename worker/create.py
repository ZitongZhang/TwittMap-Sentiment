import boto3
from tokens import endpoint

sns = boto3.resource('sns')


# When called repeatedly, the existing topic will be returned
def create_topic():
    # Creates a topic to which notifications can be published.
    topic = sns.create_topic(Name='SentimentTwitterMap')
    return topic


def subscribe(topic):
    # Subscribe end-point to the topic we just created.
    topic.subscribe(Protocol='http', Endpoint=endpoint)


if __name__ == '__main__':
    topic = create_topic()
    subscribe(topic)
