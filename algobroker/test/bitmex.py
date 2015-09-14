#!/usr/bin/python3
import algobroker
algobroker.send("control",
                [
    {
    "dest": "broker_bitmex",
    "cmd" : "loglevel",
    "level" : "DEBUG"
    }])

algobroker.send("data",
                [
    {
    "dest": "broker_bitmex",
    "cmd" : "position"
    },
    {
    "dest": "broker_bitmex",
    "cmd" : "cancel_all"
    },
    ])

"""
    {
    "dest": "broker_bitmex",
    "cmd" : "order",
    "quantity" : -10,
    "symbol" : "XBT7D",
    "price" : 241.00
    }
"""

