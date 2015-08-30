# Copyright (C) 2015 Bitquant Research Laboratories (Asia) Limited
# Released under the Simplified BSD License

import my_path
import time
import zmq
import random
import pprint
import algobroker
import algobroker.keys.plivo as plivo_keys
import msgpack
import plivo

auth_id = plivo_keys.PLIVO_AUTH_ID
auth_token = plivo_keys.PLIVO_AUTH_TOKEN
p = plivo.RestAPI(auth_id, auth_token)

def plivo():
    plivo_id = random.randrange(1,10005)
    print("I am plivo broker #%s" % (plivo_id))
    context = zmq.Context()
    # recieve work
    plivo_receiver = context.socket(zmq.PULL)
    plivo_receiver.bind(algobroker.ports.plivo)

    while True:
        pprint.pprint("read data")
        data = msgpack.unpackb(plivo_receiver.recv(),
                               encoding='utf-8')
        pprint.pprint("got_data")
        if (data['action'] == "alert" and \
            data['type'] == 'sms'):
            params = {
                'src' : plivo_keys.plivo_src_number,
                'dst' : plivo_keys.plivo_dst_number[data['dst']],
                'text' : data['text'],
                'method' : 'POST'
                }
            pprint.pprint(params)
            response = p.send_message(params)
            pprint.pprint(str(response))
        else:
            print("unknown item")
            pprint.pprint(data)
plivo()
