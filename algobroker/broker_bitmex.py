#!/usr/bin/python3
# Copyright (C) 2015 Bitquant Research Laboratories (Asia) Limited
# Released under the Simplified BSD License

import my_path
import pprint
import algobroker
from algobroker import Broker
from cryptoexchange import bitmex
import sys
import traceback

class BrokerBitmex(Broker):
    def __init__(self):
        Broker.__init__(self, "broker_bitmex")
        self.api = None
    def process_data(self, data):
        if self.api == None:
            self.error("keys not initialized")
            self.error(pprint.pformat(data))
            return
        cmd = data.get('cmd', "None")
        self.debug("processing data command %s" % cmd)
        if cmd == 'order':
            self.api.place_order(data.get('quantity', None),
                                 data.get('symbol', None),
                                 data.get('price', None))
        elif cmd == 'cancel':
            self.debug("cancelling order")
            self.api.cancel(data.get('orderID', None))
            self.debug("orders cancelled")
        elif cmd == 'cancel_all':
            self.debug("getting order list")
            orders = self.api.open_orders()
            self.debug("cancelling orders")
            for i in orders:
                self.api.cancel(i.get('orderID', None))
            self.debug("orders cancelled")
        elif cmd == "report_all":
            orders = self.api.open_orders()
            self.info(pprint.pformat(data))
        elif cmd == 'position':
            self.info(pprint.pformat(self.api.position()))
        else:
            raise RuntimeError("unknown data %s" % cmd)
    def process_control(self, data):
        if algobroker.Broker.process_control(self, data):
            return True
        cmd = data.get("cmd", "None")
        if cmd == "auth":
            self.info("received auth message")
            base_url = data.get('base_url', None)
            login = data.get('login', None)
            password = data.get('password', None)
            otpToken = data.get('otpToken', None)
            apiKey = data.get('apiKey', None)
            apiSecret = data.get('apiSecret', None)
            orderIDPrefix = data.get('orderIDPrefix', 'algo_bitmex_')
            self.api = bitmex.BitMEX(base_url,
                                     login,
                                     password,
                                     otpToken,
                                     apiKey,
                                     apiSecret,
                                     orderIDPrefix)
            try:
                self.api.authenticate()
                self.debug("get positions")
                self.debug(pprint.pformat(self.api.position()))
            except:
                self.error("Authentication error")
                self.api=None
        else:
            raise RuntimeError("unknown command %s" % cmd)

if __name__ == "__main__":
    bp = BrokerBitmex()
    bp.run()
