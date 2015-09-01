#!/usr/bin/python3
# Copyright (C) 2015 Bitquant Research Laboratories (Asia) Limited
# Released under the Simplified BSD License

import my_path
import time
import zmq
import algobroker
from algobroker import AlgoObject
import msgpack
from yahoo_finance import Share

class YahooTicker(AlgoObject):
    def __init__(self):
        AlgoObject.__init__(self, "ticker_yahoo", zmq.PUB)
        self._zmq_socket.bind(algobroker.ports.yahoo_ticker)
        self.time_limits = {}
        self.state = {}
        self.prev_state = {}
        self.assets = ["3888.HK", "0700.HK", "0388.HK"]
        self.quotes = {}
        self.sleep = 30
        self.maintainence = 60 * 30
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
            time.sleep(60)
    def send_quotes(self):
        self.debug("Sending quotes")
        self.send_message(self.quotes)
    def test(self):
        self.get_quotes()
        socket = self._context.socket(zmq.PUSH)
        socket.bind(algobroker.ports.dispatcher)
        message = { 'action' : 'log',
                    'item' : self.quotes }
        self._logger.debug("Sending data")
        socket.send(msgpack.packb(message))
    def run(self):
        self.info("Starting ticker loop")
        while True:
            self.get_quotes()
            self.send_quotes()
            time.sleep(self.sleep)

if __name__ == "__main__":
    yq = YahooTicker()
    yq.run()
