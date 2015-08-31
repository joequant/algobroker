#!/bin/bash
python3 algobroker/broker_plivo.py &
python3 algobroker/dispatcher.py &
python3 algobroker/strategy_alert.py &
python3 algobroker/quoter_yahoo.py &


