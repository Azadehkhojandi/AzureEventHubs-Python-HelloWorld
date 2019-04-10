import os
import sys
import time
from azure.eventhub import EventHubClient, Receiver, Offset


if __name__ == "__main__":

    # Address can be in either of these formats:
    # "amqps://<URL-encoded-SAS-policy>:<URL-encoded-SAS-key>@<mynamespace>.servicebus.windows.net/myeventhub"
    # "amqps://<mynamespace>.servicebus.windows.net/myeventhub"
    # SAS policy and key are not required if they are encoded in the URL

    USER = os.environ.get('EVENT_HUB_SAS_POLICY')
    KEY = os.environ.get('EVENT_HUB_SAS_KEY')
    ADDRESS = os.environ.get('EVENT_HUB_ADDRESS')
    CONSUMER_GROUP = os.environ.get('CONSUMER_GROUP')
    OFFSET = Offset(os.environ.get('OFFSET'))
    PARTITION = os.environ.get('PARTITION')
    if len(sys.argv) < 6:
        # print("Usage: python eventhub_consumer.py <eventhub_address> <eventhub_sas_policy> <eventhub_sas_key> <eventhub_consumergroup>  <eventhub_partition> <eventhub_offset>",
        #       file=sys.stderr)
        # print("Address can be in either of these formats:", "amqps://<URL-encoded-SAS-policy>:<URL-encoded-SAS-key>@<mynamespace>.servicebus.windows.net/myeventhub",
        #       "amqps://<mynamespace>.servicebus.windows.net/myeventhub")
        print("using enviornment variables")
    else:
        ADDRESS = sys.argv[1]
        USER = sys.argv[2]
        KEY = sys.argv[3]
        CONSUMER_GROUP = sys.argv[4]
        PARTITION = sys.argv[5]
        OFFSET = Offset(sys.argv[6])

    print("ADDRESS:", ADDRESS, "CONSUMER_GROUP:", CONSUMER_GROUP,
          "PARTITION:", PARTITION, "OFFSET:", OFFSET)

    PREFETCH = 100   # batch size
    total = 0
    last_sn = -1
    last_offset = "-1"
    client = EventHubClient(ADDRESS, debug=False, username=USER, password=KEY)
    try:
        receiver = client.add_receiver(
            CONSUMER_GROUP, PARTITION, prefetch=PREFETCH, offset=OFFSET)
        client.run()

        batch = receiver.receive(timeout=1)

        while True:
            for event_data in batch:
                
                last_offset = event_data.offset
                last_sn = event_data.sequence_number
                print("Msg offset: " + str(last_offset))
                print("Msg seq: " + str(last_sn))
                print("Msg body: " + event_data.body_as_str())
                total += 1
            batch = receiver.receive(timeout=1)

    except KeyboardInterrupt:
        pass

    finally:
        client.stop()
