#!/usr/bin/python3
# Copyright (C) 2015 Bitquant Research Laboratories (Asia) Limited
# Released under the Simplified BSD License
import my_path
import time
import algobroker
import pprint

class StrategyXbtClose(algobroker.Strategy):
    def __init__(self):
        algobroker.Strategy.__init__(self, "strategy_xbt_close",
                                     ['ticker_bravenewcoin'])
        self.range = 0.01
        self.xbt_initial_price = None
        self.xbt_current_price = None
        self.active = True
        self.set_logger_level("DEBUG")
        self.send_control("ticker_bravenewcoin",
                          {"cmd" : "set",
                           "assets" : ['btc_usd_24hr']})
    def send_cancel(self):
        msg = "XBT orders cancelled"
        self.send_action({'cmd' : 'alert',
                          'type' : 'sms',
                          'to' : 'trader1',
                          'text' : msg})
        self.send_action({'cmd' : 'cancel_all',
                          'broker' : 'bitmex'})
        self.active = False
        self.xbt_initial_price = None
    def process_control(self, data):
        if algobroker.Strategy.process_control(self, data):
            return
        if data['cmd'] == "set":
            if 'range' in data:
                self.range = data['limits']
        elif data['cmd'] == 'activate':
            self.active = True
            if self.xbt_current_price != None:
                self.xbt_initial_price = self.xbt_current_price
    def process_data(self, data):
        if 'btc_usd_24hr' in data and 'last' in data['btc_usd_24hr']:
            self.xbt_current_price = float(data['btc_usd_24hr']['last'])
            if self.xbt_initial_price == None:
                self.debug("setting price to %f" % self.xbt_current_price)
                self.xbt_initial_price = self.xbt_current_price
        if (self.xbt_current_price < \
            self.xbt_initial_price * (1 - self.range) or
            self.xbt_current_price > \
            self.xbt_initial_price * (1 + self.range)):
            self.send_cancel()

if __name__ == "__main__":
    qm = StrategyXbtClose()
    qm.run()
