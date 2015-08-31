#!/usr/bin/python3
# Copyright (C) 2015 Bitquant Research Laboratories (Asia) Limited
# Released under the Simplified BSD License
import my_path
import time
import zmq
import algobroker
import msgpack
from yahoo_finance import Share

class YahooQuoter(object):
    def __init__(self):
        self.time_limits = {}
        self.state = {}
        self.prev_state = {}
        self.assets = ["3888.HK", "0700.HK", "0388.HK"]
        self.quotes = {}
        self.sleep = 30
        self.maintainence = 60 * 30
        self._context = zmq.Context()
        self._zmq_socket = self._context.socket(zmq.PUB)
        self._zmq_socket.bind(algobroker.ports.yahoo_quoter)
    def send_message(self, message):
        self._zmq_socket.send(msgpack.packb(message))
    def get_quotes(self):
        print("getting quotes")
        try:
            for i in self.assets:
                yahoo = Share(i)
                self.quotes[i] = {
                    "source" : "yahoo",
                    "last" : float(yahoo.get_price())
                    }
        except OSError:
            print("Network Error")
            time.sleep(60)
    def send_quotes(self):
        print("sending quotes")
        self.send_message(self.quotes)
    def test(self):
        self.get_quotes()
        socket = self._context.socket(zmq.PUSH)
        socket.bind(algobroker.ports.dispatcher)
        message = { 'action' : 'log',
                    'item' : self.quotes }
        print("sending data")
        socket.send(msgpack.packb(message))
    def run(self):
        while True:
            self.get_quotes()
            self.send_quotes()
            time.sleep(self.sleep)

if __name__ == "__main__":
    yq = YahooQuoter()
    yq.run()
