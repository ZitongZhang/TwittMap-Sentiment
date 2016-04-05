import boto3
def createTopic (client, topicName):
    # Creates a topic to which notifications can be published.
    response = client.create_topic(
        Name=topicName
    )

    topicArn = response['TopicArn']

    # Subscribe end-point to the topic we just created.
    response = client.subscribe(
        TopicArn=topicArn,
        Protocol='http',
        Endpoint='http://ec2-52-201-216-88.compute-1.amazonaws.com'
    )
    return topicArn