import json
from threading import Thread, Event
import sys
import os

print(sys.executable)
from azure.eventhub import EventHubClient, Sender, EventData
from producer import ProducerThread


def listener(message):
    print(message)
    sender.send(EventData(message))


if __name__ == "__main__":

    INTERVAL_IN_SECONDS = os.environ.get('INTERVAL_IN_SECONDS')
    STREAM_ID = os.environ.get('STREAM_ID')

    # Address can be in either of these formats:
    # "amqps://<URL-encoded-SAS-policy>:<URL-encoded-SAS-key>@<mynamespace>.servicebus.windows.net/myeventhub"
    # "amqps://<mynamespace>.servicebus.windows.net/myeventhub"
    # SAS policy and key are not required if they are encoded in the URL
    ADDRESS = os.environ.get('EVENT_HUB_ADDRESS')
    USER = os.environ.get('EVENT_HUB_SAS_POLICY')
    KEY = os.environ.get('EVENT_HUB_SAS_KEY')
    PARTITION = os.environ.get('PARTITION')

    if len(sys.argv) < 6:
        print("using enviornment variables")
    else:
        INTERVAL_IN_SECONDS = sys.argv[1]
        STREAM_ID = sys.argv[2]
        ADDRESS = sys.argv[3]
        USER = sys.argv[4]
        KEY = sys.argv[5]
        PARTITION = sys.argv[6]
    if not ADDRESS:
        raise ValueError("No EventHubs URL supplied.")

    print("INTERVAL_IN_SECONDS:", INTERVAL_IN_SECONDS,
          "STREAM_ID:", STREAM_ID, "ADDRESS:", ADDRESS)

    client = EventHubClient(ADDRESS, debug=False, username=USER, password=KEY)
    sender = client.add_sender(partition=PARTITION)
    client.run()

    thread = ProducerThread(listener, STREAM_ID, float(INTERVAL_IN_SECONDS))
