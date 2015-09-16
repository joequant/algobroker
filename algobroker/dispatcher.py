#!/usr/bin/python3
# Copyright (C) 2015 Bitquant Research Laboratories (Asia) Limited
# Released under the Simplified BSD License

import my_path
import time
import zmq.green as zmq
import pprint
import algobroker
import msgpack

class Dispatcher(algobroker.Broker):
    def __init__(self):
        algobroker.Broker.__init__(self, "dispatcher")
        # send work
        self.sms_sender = self.socket(zmq.PUSH)
        self.sms_sender.connect(algobroker.ports['data']['broker_plivo'])
        self.bitmex_sender = self.socket(zmq.PUSH)
        self.bitmex_sender.connect(algobroker.ports['data']['broker_bitmex'])
    def process_data(self, data):
        if (data['cmd'] == "log"):
            self.warning(pprint.pformat(data))
        elif (data['cmd'] == 'alert' and \
              data['type'] == 'sms'):
            self.debug("sending sms")
            self.debug(pprint.pformat(data))
            self.sms_sender.send(msgpack.packb(data))
        elif (data['broker'] == 'bitmex'):
            self.debug("sending bitmex")
            self.debug(pprint.pformat(data))
            self.bitmex_sender.send(msgpack.packb(data))
        else:
            self.error("unknown action")

if __name__ == "__main__":
    dispatcher = Dispatcher()
    dispatcher.run()

