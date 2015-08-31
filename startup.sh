#!/bin/bash
python3 algobroker/plivo_broker.py &
python3 algobroker/dispatcher.py &
python3 algobroker/quote_monitor.py &


