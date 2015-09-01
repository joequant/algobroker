#!/usr/bin/python3
# Copyright (C) 2015 Bitquant Research Laboratories (Asia) Limited
# Released under the Simplified BSD License

import my_path
import pprint
import algobroker
from algobroker import Broker
import algobroker.keys.plivo as plivo_keys
import plivo

class BrokerPlivo(Broker):
    def __init__(self):
        Broker.__init__(self, "broker_plivo",
                        algobroker.ports.plivo)
        self.auth_id = plivo_keys.PLIVO_AUTH_ID
        self.auth_token = plivo_keys.PLIVO_AUTH_TOKEN
        self.api = plivo.RestAPI(self.auth_id, self.auth_token)
    def process_request(self, data):
        if (data['action'] == "alert" and \
            data['type'] == 'sms'):
            params = {
                'src' : plivo_keys.plivo_src_number,
                'dst' : plivo_keys.plivo_dst_number[data['dst']],
                'text' : data['text'],
                'method' : 'POST'
                }
            self.debug(pprint.pformat(params))
            response = self.api.send_message(params)
            self.debug(pprint.pformat(str(response)))
        else:
            self.error("unknown item")
            self.error(pprint.pformat(data))

if __name__ == "__main__":
    bp = BrokerPlivo()
    bp.run()
