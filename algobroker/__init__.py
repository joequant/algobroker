# Copyright (C) 2015 Bitquant Research Laboratories (Asia) Limited
# Released under the Simplified BSD License

import logging
import zmq
import msgpack
import time

def logger(s : str):
    logger = logging.getLogger(s)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter.converter = time.gmtime
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

class AlgoObject(object):
    def __init__(self, name : str, socket_type):
        self._context = zmq.Context()
        self._zmq_socket = self.socket(socket_type)
        self._logger = logger(name)
        self.info("starting %s" % name)
    def socket(self, socket_type):
        return self._context.socket(socket_type)
    def send_message(self, message):
        self._zmq_socket.send(msgpack.packb(message))
    def recv_message(self):
        return msgpack.unpackb(self._zmq_socket.recv(),
                               encoding='utf-8')
    def debug(self, s):
        self._logger.debug(s)
    def info(self, s):
        self._logger.info(s)
    def error(self, s):
        self._logger.error(s)
    def warning(self, s):
        self._logger.warning(s)

class Broker(AlgoObject):
    def __init__(self, name, port):
        AlgoObject.__init__(self, name, zmq.PULL)
        self._zmq_socket.bind(port)
    def run(self):
        while True:
            self.debug("waiting for data")
            data = self.recv_message()
            self.debug("got_data")
            self.process_request(data)
    def process_request(self, data):
        raise NotImplementedError

        
class ports(object):
    dispatcher = "tcp://127.0.0.1:5557"
    plivo = "tcp://127.0.0.1:5558"
    alert_set_quote = "tcp://127.0.0.1:5559"
    yahoo_ticker = "tcp://127.0.0.1:5560"
    bitfutures_ticker = "tcp://127.0.0.1:5560"

    
