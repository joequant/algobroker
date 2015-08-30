#!/usr/bin/python3
import time
import zmq
import algobroker
import msgpack

from algobroker.quote_monitor import QuoteMonitor

if __name__ == "__main__":
    qm = QuoteMonitor()
    qm.test1()
