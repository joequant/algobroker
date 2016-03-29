#!/usr/bin/python3

import json
import sys
import algobroker

filename = sys.argv[1]
print("reading %s" % filename)

with open(filename) as json_data:
    d = json.load(json_data)
    json_data.close()
    algobroker.send(d)
