#!/usr/bin/python3
import algobroker
algobroker.send("control",
                [
    {"dest": "ticker_yahoo",
     "cmd" : "set",     
     "assets" : ["3888.HK", "0700.HK", "0388.HK"]
     },
    {"dest": "broker_bitmex",
     "cmd" : "loglevel",
     "level" : "DEBUG"
    },
    {"dest": "ticker_bitfutures",
     "cmd" : "loglevel",
     "level" : "DEBUG"
    },
    {"dest": "ticker_bitfutures",
     "cmd" : "set",
     "exchanges" : ["bitmex"]
    },
    {"dest": "strategy_alert",
     "cmd" : "set",
     "limits" : {
    "3888.HK" : [ 14.8, 15.5],	
    "0700.HK" : [ 125.0, 130.0],
    "0388.HK" : [ 175.0, 180.0]
    }
    }
    ])

