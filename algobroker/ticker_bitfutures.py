#!/usr/bin/python3
# Copyright (C) 2015 Bitquant Research Laboratories (Asia) Limited
# Released under the Simplified BSD License

import my_path
import time
import zmq
import algobroker
from algobroker import AlgoObject
import msgpack
import bitfutures

class BitfuturesTicker(AlgoObject):
    def __init__(self):
        AlgoObject.__init__(self, "ticker_bitfutures", zmq.PUB)
        self._data_socket.bind(algobroker.data_ports["ticker_bitfutures"])
        self.exchanges = ["bitmex"]
        self.time_limits = {}
        self.state = {}
        self.prev_state = {}
        self.quotes = {}
        self.sleep = 30
        self.maintainence = 60 * 30
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
                            "ask" : float(k[1]),
                            "bid" : float(k[2]),
                            "last" : float(k[3])
                            }
            self.debug(self.quotes)
        except OSError:
            self.error("Network Error")
            time.sleep(60)
    def send_quotes(self):
        self.debug("Sending quotes")
        self.send_data(self.quotes)
    def test(self):
        self.get_quotes()
        socket = self._context.socket(zmq.PUSH)
        socket.connect(algobroker.data_ports['dispatcher'])
        message = { 'action' : 'log',
                    'item' : self.quotes }
        self._logger.debug("Sending data")
        socket.send(msgpack.packb(message))
    def run_once(self):
        self.debug("running loop function")
        self.get_quotes()
        self.send_quotes()

if __name__ == "__main__":
    yq = BitfuturesTicker()
    yq.run()
