# Introduction 
Producer generates stream of data 

Json body

unquie Identifier 
timespan
random number between 0-100

Example of message: 

```
{"id": "bananas", "utc": "April 10 2019 - 01:49:42", "timestamp": 1554860982.597929, "value": 26}
```
## Quick start

1. gets the images from docker hub
`docker pull azadehkhojandi/azure_eventhub_mock_producer:0.1`
`docker pull azadehkhojandi/azure_eventhub_consumer:0.1`

2. run the images 

produces creates a mock data and push it into event hub

`docker run --env INTERVAL_IN_SECONDS=2 --env STREAM_ID=sensor1  --env EVENT_HUB_SAS_POLICY=insert-your-policy-name --env EVENT_HUB_SAS_KEY=insert-your-key  --env EVENT_HUB_ADDRESS=amqps://insert-your-eventhubnamespace-name.servicebus.windows.net/insert-your-eventhub-name   --env PARTITION=0  --env PYTHONUNBUFFERED=0 azadehkhojandi/azure_eventhub_mock_producer:0.1`


consumer reads it from the stream

`docker run --env EVENT_HUB_SAS_POLICY=insert-your-policy-name --env EVENT_HUB_SAS_KEY=insert-your-key  --env EVENT_HUB_ADDRESS=amqps://insert-your-eventhubnamespace-name.servicebus.windows.net/insert-your-eventhub-name --env CONSUMER_GROUP=\$default --env OFFSET=-1 --env PARTITION=0  --env PYTHONUNBUFFERED=0  azadehkhojandi/azure_eventhub_consumer:0.1`



### How to:
1. Get linux version? `cat /etc/os-release`
2. Create Conda environment based on `environment.yml` file?`conda env create -f environment.yml`
3. Update the `environment.yml` file?  `conda env export > environment.yml`
4. To solve Python app does not print anything when running detached in docker, set enviornment varibale `PYTHONUNBUFFERED=0`
5. To solve below error on WSL

    `Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?`

    `docker -H tcp://0.0.0.0:2375 images`
    
    `echo "export DOCKER_HOST='tcp://0.0.0.0:2375'" >> ~/.bashrc`
    
    `source ~/.bashrc`


### Producer

It produces mock/dummy messages and sends it to eventhub stream


1. build the docker image

`docker build -t mocks/eventhub_producer:0.1 -f producer.Dockerfile .`

2. run the docker image

option 1: 

`docker run --env INTERVAL_IN_SECONDS=2 --env STREAM_ID=sensor1  --env EVENT_HUB_SAS_POLICY=insert-your-policy-name --env EVENT_HUB_SAS_KEY=insert-your-key  --env EVENT_HUB_ADDRESS=amqps://insert-your-eventhubnamespace-name.servicebus.windows.net/insert-your-eventhub-name   --env PARTITION=0  --env PYTHONUNBUFFERED=0 mocks/eventhub_producer:0.1`

option 2:

`docker run --env-file ./producer.env.list mocks/eventhub_producer:0.1`

Note: You can overwrite env variables in env-file by passing them directly 

`docker run --env-file ./producer.env.list -e STREAM_ID=testazadeh  mocks/eventhub_producer:0.1`

### Consumer

It reads the  messages from eventhub stream

`docker pull azadehkhojandi/azure_eventhub_consumer:0.1``

1. build the docker image

`docker build -t mocks/eventhub_consumer:0.1 -f consumer.Dockerfile .`

2. run the docker image

option 1: 

`docker run --env EVENT_HUB_SAS_POLICY=insert-your-policy-name --env EVENT_HUB_SAS_KEY=insert-your-key  --env EVENT_HUB_ADDRESS=amqps://insert-your-eventhubnamespace-name.servicebus.windows.net/insert-your-eventhub-name --env CONSUMER_GROUP=\$default --env OFFSET=-1 --env PARTITION=0  --env PYTHONUNBUFFERED=0  mocks/eventhub_consumer:0.1`

option 2:

`docker run --env-file ./consumer.env.list mocks/eventhub_consumer:0.1`

Note: You can overwrite env variables in env-file by passing them directly 

`docker run --env-file ./consumer.env.list -e CONSUMER_GROUP=insert_your_customgroup_name  mocks/eventhub_consumer:0.1`


# Resources
    1. Build a Docker image and push it to an Azure Container Registry. 
    https://docs.microsoft.com/azure/devops/pipelines/languages/docker

# Loging to ACR
`az login`

`az account set --subscription insert-your-subscription-id`

`az acr login -n insert-your-acr-name`

`docker pull insert-your-acr-name.azurecr.io/streams/eventhub-mock-producer`

`docker pull insert-your-acr-name.azurecr.io/streams/eventhub-consumer`

`docker run --env-file ./producer.env.list insert-your-acr-name.azurecr.io/streams/eventhub-mock-producer`

`docker run --env-file ./consumer.env.list insert-your-acr-name.azurecr.io/streams/eventhub-consumer`
