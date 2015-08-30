# Copyright (C) 2015 Bitquant Research Laboratories (Asia) Limited
# Released under the Simplified BSD License

import time
import zmq
import random
import pprint
import algobroker
import msgpack

def dispatcher():
    dispatcher_id = random.randrange(1,10005)
    print("I am dispatcher #%s" % (dispatcher_id))
    context = zmq.Context()
    # recieve work
    dispatcher_receiver = context.socket(zmq.PULL)
    dispatcher_receiver.connect(algobroker.ports.dispatcher)
    # send work
    sms_sender = context.socket(zmq.PUSH)
    sms_sender.connect(algobroker.ports.plivo)

    while True:
        data = msgpack.unpackb(dispatcher_receiver.recv(),
                               encoding='utf-8')
        if (data['action'] == "log"):
            print("Log")
            pprint.pprint(data)
        elif (data['action'] == 'alert' and \
              data['type'] == 'sms'):
            pprint.pprint(data)
            sms_sender.send(msgpack.packb(data))
        else:
            print("unknown action")

dispatcher()
