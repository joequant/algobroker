#!/usr/bin/python3
# Copyright (C) 2015 Bitquant Research Laboratories (Asia) Limited
# Released under the Simplified BSD License

import my_path
import pprint
import algobroker
from algobroker import Broker
import twilio

class BrokerTwilio(Broker):
    def __init__(self):
        Broker.__init__(self, "broker_twilio")
        self.api = None
        self.src_number = None
        self.dst_number = None
    def process_data(self, data):
        if self.api == None or \
           self.src_number == None or \
           self.dst_number == None:
            self.error("keys not initialized")
        if (data['cmd'] == "alert" and \
            data['type'] == 'sms'):
            params = {
                'from' : self.src_number,
                'to' : self.dst_number[data['to']],
                'body' : data['text'],
                }
            self.debug(pprint.pformat(params))
            response = self.api.messages.create(**params)
            self.debug(pprint.pformat(str(response)))
        else:
            self.error("unknown item")
            self.error(pprint.pformat(data))
    def process_control(self, data):
        algobroker.Broker.process_control(self, data)
        if data.get('cmd', None) == "auth":
            self.auth_id = data['TWILIO_AUTH_ID']
            self.auth_token = data['TWILIO_AUTH_TOKEN']
            self.api = twilio.rest.TwilioRestClient(self.auth_id,
                                                    self.auth_token)
            self.src_number = data['src_number']
            self.dst_number = data['dst_number']

if __name__ == "__main__":
    bp = BrokerTwilio()
    bp.run()
