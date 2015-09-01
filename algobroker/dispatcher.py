#!/usr/bin/python3
# Copyright (C) 2015 Bitquant Research Laboratories (Asia) Limited
# Released under the Simplified BSD License

import my_path
import time
import zmq
import pprint
import algobroker
import msgpack
from algobroker import Broker

class Dispatcher(Broker):
    def __init__(self):
        Broker.__init__(self, "dispatcher", 
                        algobroker.ports.dispatcher)
        # send work
        self.sms_sender = self.socket(zmq.PUSH)
        self.sms_sender.connect(algobroker.ports.plivo)
    def process_request(self, data):
        if (data['action'] == "log"):
            self.warning(pprint.pformat(data))
        elif (data['action'] == 'alert' and \
              data['type'] == 'sms'):
            self.debug("sending sms")
            self.debug(pprint.pformat(data))
            self.sms_sender.send(msgpack.packb(data))
        else:
            self.error("unknown action")

if __name__ == "__main__":
    dispatcher = Dispatcher()
    dispatcher.run()

