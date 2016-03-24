#!/usr/bin/python3
# Copyright (C) 2015 Bitquant Research Laboratories (Asia) Limited
# Released under the Simplified BSD License

import my_path
import time
import algobroker
import exchanges
import pprint
import threading

data_lock = threading.Lock()

class BitcoinThread(threading.Thread):
    def __init__(self, exchange_name, ticker, delay=1000):
        threading.Thread.__init__(self)
        self.exchange_name = exchange_name
        self.ticker = ticker
        self.api = exchanges.get_exchange(exchange_name)
        self.delay = delay
        self.runloop = True
    def run(self):
        while self.runloop:
            self.api.refresh()
            data_lock.acquire()
            self.ticker.exchange_data[self.exchange_name] = self.api.get_current_data()
            data_lock.release()
            time.sleep(self.delay/1000.0)
    def stop(self):
        self.runloop = False

class BitcoinTicker(algobroker.Ticker):
    def __init__(self):
        algobroker.Ticker.__init__(self, "ticker_bitcoin")
        self.exchanges = {}
        self.time_limits = {}
        self.state = {}
        self.prev_state = {}
        self.exchange_threads = {}
        self.exchange_data = {}
        self.timeout = 5000
        self.thread_delay = 1000
    def get_quotes(self):
        self.debug("getting quotes")
        self.debug(self.exchange_data)
        self.quotes = self.exchange_data
    def process_control(self, data):
        if algobroker.Ticker.process_control(self, data):
            return True
        elif data['cmd'] == "set":
            if 'exchanges' in data:
                self.exchange_data = {}
                self.debug("stopping threads")
                for t in self.exchange_threads.values():
                    t.stop()
                self.debug("setting exchange list")
                self.debug(pprint.pformat(data['exchanges']))
                for e in data['exchanges']:
                    self.exchange_threads[e] = BitcoinThread(e,
                                                             self,
                                                             self.thread_delay)
                    self.exchange_threads[e].start()
        elif data['cmd'] == "test":
            self.debug("received test message")
            self.test()
        else:
            raise RuntimeError("unknown command %s" % data['cmd'])

if __name__ == "__main__":
    yq = BitcoinTicker()
    yq.run()
