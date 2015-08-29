#!/usr/bin/python
import zerorpc
from algobroker import AlgoBroker

s = zerorpc.Server(AlgoBroker())
s.bind("tcp://0.0.0.0:4242")
s.run()
