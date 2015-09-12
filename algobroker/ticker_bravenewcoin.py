#!/usr/bin/python3
# Copyright (C) 2015 Bitquant Research Laboratories (Asia) Limited
# Released under the Simplified BSD License

import my_path
import time
import zmq
import algobroker
from algobroker import AlgoObject
import msgpack
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

class BraveNewCoinTicker(AlgoObject):
    def __init__(self):
        AlgoObject.__init__(self, "ticker_bravenewcoin", zmq.PUB)
        self._data_socket.bind(algobroker.data_ports["ticker_bravenewcoin"])
        self.time_limits = {}
        self.state = {}
        self.prev_state = {}
        self.assets = []
        self.quotes = {}
        self.timeout = 30000
        self.sleep = 30
        self.maintainence = 60 * 30
    def get_quotes(self):
        self.debug("getting quotes")
        try:
            for i in self.assets:
                res = requests.get("http://api.bravenewcoin.com/ticker/bnc_ticker_%s.json" % i)
                self.quotes[i] =  { newkey(key):value for key,value in res.json().items() }
        except OSError:
            self.error("Network Error")
    def send_quotes(self):
        self.debug("Sending quotes")
        self.send_data(self.quotes)
    def test(self):
        self.get_quotes()
        socket = self._context.socket(zmq.PUSH)
        socket.bind(algobroker.ports.dispatcher)
        message = { 'action' : 'log',
                    'item' : self.quotes }
        self._logger.debug("Sending data")
        socket.send(msgpack.packb(message))
    def process_control(self, data):
        self.debug("received control message")
        if data['cmd'] == "set":
            if 'assets' in data:
                self.debug("setting asset list")
                self.debug(pprint.pformat(data['assets']))
                self.assets = data['assets']
    def run_once(self):
        self.debug("running loop function")
        self.get_quotes()
        self.send_quotes()

if __name__ == "__main__":
    bnct = BraveNewCoinTicker()
    bnct.run()
