from threading import Thread, Event
import random
import json
import datetime
import sys
import threading
import os

from threading import Timer

class ProducerThread(object):
    def __init__(self,  callback, id, interval=1, min_value=1, max_value=100):
        self._timer     = None
        self.interval   = interval
        self.function   = callback
        self.id = id
        self.min_value = min_value
        self.max_value = max_value
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        message = {
            "id": self.id,
            "value": random.randint(self.min_value, self.max_value),
            "timestamp": datetime.datetime.utcnow().timestamp(),
            "utc": datetime.datetime.utcnow().strftime('%B %d %Y - %H:%M:%S')
        }
        # convert into JSON:
        json_msg = json.dumps(message)
        # call callback\delegate function
        self.function(json_msg)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


