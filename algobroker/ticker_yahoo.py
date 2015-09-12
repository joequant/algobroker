#!/usr/bin/python3
# Copyright (C) 2015 Bitquant Research Laboratories (Asia) Limited
# Released under the Simplified BSD License

import my_path
import time
import algobroker
import pprint
from yahoo_finance import Share

class YahooTicker(algobroker.Ticker):
    def __init__(self):
        algobroker.Ticker.__init__(self, "ticker_yahoo")
        self.time_limits = {}
        self.state = {}
        self.prev_state = {}
        self.assets = []
    def get_quotes(self):
        self.debug("getting quotes")
        try:
            for i in self.assets:
                yahoo = Share(i)
                self.quotes[i] = {
                    "source" : "yahoo",
                    "last" : float(yahoo.get_price())
                    }
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
    yq = YahooTicker()
    yq.run()
