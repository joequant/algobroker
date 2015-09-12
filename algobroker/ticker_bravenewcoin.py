#!/usr/bin/python3
# Copyright (C) 2015 Bitquant Research Laboratories (Asia) Limited
# Released under the Simplified BSD License

import my_path
import time
import algobroker
import pprint
import requests

def newkey(s):
    if s == "last_price":
        return "last"
    elif s == "open_price":
        return "open"
    elif s == "low_price":
        return "low"
    elif s == "high_price":
        return "high"
    else:
        return str(s)

class BraveNewCoinTicker(algobroker.Ticker):
    def __init__(self):
        algobroker.Ticker.__init__(self, "ticker_bravenewcoin")
        self.time_limits = {}
        self.state = {}
        self.prev_state = {}
        self.assets = []
    def get_quotes(self):
        self.debug("getting quotes")
        try:
            for i in self.assets:
                res = requests.get("http://api.bravenewcoin.com/ticker/bnc_ticker_%s.json" % i)
                self.quotes[i] =  { newkey(key):value for key,value in res.json().items() }
        except OSError:
            self.error("Network Error")
    def process_control(self, data):
        algobroker.Ticker.process_control(self, data)
        if data['cmd'] == "set":
            if 'assets' in data:
                self.debug("setting asset list")
                self.debug(pprint.pformat(data['assets']))
                self.assets = data['assets']

if __name__ == "__main__":
    bnct = BraveNewCoinTicker()
    bnct.run()
