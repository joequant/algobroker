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

class StrategyAlert(AlgoObject):
    def __init__(self):
        AlgoObject.__init__(self, "strategy_alert", zmq.SUB)
        self._data_socket.connect(algobroker.data_ports['ticker_yahoo'])
        self._data_socket.setsockopt(zmq.SUBSCRIBE, b'')
        self.time_limits = {}
        self.state = {}
        self.prev_state = {}
        self.limits = {}
        self.quotes = {}
        self.maintainence = 60 * 30
        self._action_socket = self.socket(zmq.PUSH)
        self._action_socket.connect(algobroker.data_ports['dispatcher'])
    def test_limits(self):
        for i in self.limits.keys():
            if i in self.limits and i in self.quotes:
                limits = self.limits[i]
                if limits[0] != None and self.quotes[i] <= limits[0]:
                    self.state[i] = "low"
                elif limits[1] != None and self.quotes[i] >= limits[1]:
                    self.state[i] = "high"
                else:
                    self.state[i] = "ok"
    def send_action(self, message):
        self._action_socket.send(msgpack.packb(message))
    def send_notices(self):
        msg = ""
        for k, v in self.state.items():
            if k in self.prev_state:
                prev_state = self.prev_state[k]
            else:
                prev_state = "none"
            if v == "high" or v == "low":
                if prev_state == "ok" or prev_state == "none":
                    msg += "%s - %f - %s | " % (k, self.quotes[k],
                                                v)
        if msg != "":
            self.send_action({'action' : 'alert',
                              'type' : 'sms',
                              'dst' : 'trader1',
                              'text' : msg})
        for k, v in self.state.items():
            self.prev_state[k] = v
    def test(self):
        work_message = { 'action' : 'log',
                         'item' : 'hello' }
        self.send_action(work_message)
        work_message = { 'action' : 'alert',
                         'type' : 'sms',
                         'dst'  : 'trader1',
                         'text' : 'hello and happy trading' }
        self.send_action(work_message)
    def process_control(self, data):
        self.debug("getting control data")
        if data['cmd'] == "set":
            if 'limits' in data:
                self.debug("setting limits")
                self.debug(pprint.pformat(data))
                self.limits = data['limits']
    def process_data(self, data):
        self.info("running alert loop")
        self.info(data)
        for k, v in data.items():
            self.quotes[k] = data[k]['last']
        self.test_limits()
        self.send_notices()

if __name__ == "__main__":
    qm = StrategyAlert()
    qm.run()
