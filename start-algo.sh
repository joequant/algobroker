#!/bin/bash
python3 algobroker/broker_plivo.py &
python3 algobroker/broker_bitmex.py &
python3 algobroker/broker_twilio.py &
python3 algobroker/dispatcher.py &
python3 algobroker/strategy_alert.py &
python3 algobroker/strategy_xbt_close.py &
python3 algobroker/ticker_yahoo.py &
python3 algobroker/ticker_bitcoin.py &
python3 algobroker/broker_web.py &




