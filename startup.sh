#!/bin/bash
python3 algobroker/plivo_broker.py &
python3 algobroker/dispatcher.py &
python3 algobroker/alert.py &
python3 algobroker/yahoo_quoter.py &


