#!/usr/bin/python3
# Copyright (C) 2015 Bitquant Research Laboratories (Asia) Limited
# Released under the Simplified BSD License
import my_path
import time
import zmq
import algobroker
import msgpack

from algobroker.quote_monitor import QuoteMonitor

if __name__ == "__main__":
    qm = QuoteMonitor()
    qm.test1()
