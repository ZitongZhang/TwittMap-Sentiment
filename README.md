# TwittMap-Sentiment
Assignment 2 for COMS E6998 Cloud Computing and Big Data

## Step 1: Setting Up Amazon Elasticsearch
* Run the following command to create a domain:
```
aws es create-elasticsearch-domain --domain-name twittmap --elasticsearch-cluster-config InstanceType=t2.micro.elasticsearch,InstanceCount=1 --ebs-options EBSEnabled=true,VolumeType=gp2,VolumeSize=10
```
* For simplicity, configure the access policy to allow open access to the domain (of course this shouldn't be used in reality)
* Run the following command. This creates a index (database) called *twittmap* and a type (table) called *tweets*.
```
curl -XPUT <Elasticsearch Endpoint>/twittmap -d '
{
    "mappings": {
        "tweets": {
            "properties": {
                "user": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "time": {
                    "type": "date"
                },
                "text": {
                    "type": "string"
                },
                "geo": {
                    "type": "geo_point"
                },
                "sentiment": {
                    "type": "string"
                }
            }
        }
    }
}'
```

## Step 2: Launching the Backend
* Create an EC2 instance
* Pull the repo from Github, `cd` into `nodejs`, and run `npm install` to install the needed packages
* Modify the Elasticsearch endpoint in `app.js`
* Run `sudo node app.js &` (`sudo` is necessary since we are listening on port 80)

## Step 3: Launching the Streaming Server
* `cd` into `streaming`
* Create a Python file `tokens.py` that stores the keys for Twitter. It should look like this:
```
consumer_key = '???'
consumer_secret = '???'
access_token = '???'
access_token_secret = '???'
```
* Set up AWS CLI on the instance
* Run `pip install -r requirements.txt` to install the needed packages
* Run `python create.py` once
* Run `python streaming.py &`

## Step 4: Launching the Worker
* `cd` into `worker`
* Create a text file `api_key.txt` that contains the key for AlchemyAPI
* Create a Python file `tokens.py` that contains a single variable `endpoint`, which stores the endpoint of the backend
* Run `pip install -r requirements.txt` to install the needed packages
* Run `python create.py` once
* Run `python worker.py &`