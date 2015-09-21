#!/usr/bin/python3
# Copyright (C) 2015 Bitquant Research Laboratories (Asia) Limited
# Released under the Simplified BSD License

import my_path
import time
import algobroker
from cryptoexchange import bitfutures
import pprint

class BitfuturesTicker(algobroker.Ticker):
    def __init__(self):
        algobroker.Ticker.__init__(self, "ticker_bitfutures")
        self.exchanges = []
        self.time_limits = {}
        self.state = {}
        self.prev_state = {}
    def get_quotes(self):
        self.debug("getting quotes")
        data = bitfutures.get_data(self.exchanges)
        try:
            data = data['futures']
            for i in self.exchanges:
                if i in data:
                    j = data[i]
                    self.debug(j)
                    for k in zip(j['dates'],
                                 j['asks'],
                                 j['bids'],
                                 j['last'],
                                 j['contract']):
                        tag = k[4] + "." + k[0].replace("-", "") + "." + i
                        self.quotes[tag] = {
                            "ask" : float(k[1]) if k[1] != None else None,
                            "bid" : float(k[2]) if k[2] != None else None,
                            "last" : float(k[3]) if k[3] != None else None,
                            }
            self.debug(self.quotes)
        except OSError:
            self.error("Network Error")
            time.sleep(60)
    def process_control(self, data):
        algobroker.Ticker.process_control(self, data)
        if data['cmd'] == "set":
            if 'exchanges' in data:
                self.debug("setting exchange list")
                self.debug(pprint.pformat(data['exchanges']))
                self.exchanges = data['exchanges']
        elif data['cmd'] == "test":
            self.debug("received test message")
            self.test()

if __name__ == "__main__":
    yq = BitfuturesTicker()
    yq.run()
