#!/usr/bin/python3
# Copyright (C) 2015 Bitquant Research Laboratories (Asia) Limited
# Released under the Simplified BSD License

import datetime
def weekly_expiry():
    d = datetime.date.today()
    while d.weekday() != 5:
        d += datetime.timedelta(1)
    return d

def  quarter_expiry():
    ref = datetime.date.today()
    if ref.month < 4:
        d = datetime.date(ref.year, 3, 31)
    elif ref.month < 7:
        d = datetime.date(ref.year, 6, 30)
    elif ref.month < 10:
        d = datetime.date(ref.year, 9, 30)
    else:
        d= datetime.date(ref.year, 12, 31)
    while d.weekday() != 5:
        d -= datetime.timedelta(1)
    return d
quarter_expiry()

def date_stamp(d):
    return d.strftime("%Y-%m-%d")

def time_stamp(d):
    return d.strftime("%H:%M:%S")

import json
import requests
import dateutil.parser
import pprint
import numpy as np

#usdcny = requests.get('http://rate-exchange.appspot.com/currency?from=USD&to=CNY').json()['rate']
usdcny = 6.41



def get_data(exchanges=None):
    retval = {}
    expiry = {}
    futures = {}
    expiry['week'] = weekly_expiry()
    expiry['next_week'] = weekly_expiry() + datetime.timedelta(7)
    expiry['quarter'] = quarter_expiry()
    retval['spot'] = {}

    bitFinexTick = requests.get("https://api.bitfinex.com/v1/ticker/btcusd")
    retval['spot']['bitfinex'] = bitFinexTick.json()['last_price']
    #bitmex
    if (exchanges == None or "bitmex" in exchanges):
        data = requests.get('https://www.bitmex.com:443/api/v1/instrument/active').json()
        symbols = []
        dates = []
        bids = []
        asks = []
        last = []
        contract = []
        for contracttype in ["XBU", "XBT"]:
            for i in data:
                if i['rootSymbol'] == contracttype and i['buyLeg'] == "":
                    dates.append(date_stamp(dateutil.parser.parse(i['expiry'])))
                    symbols.append(i['symbol'])
                    bids.append(i['bidPrice'])
                    asks.append(i['askPrice'])
                    last.append(i['lastPrice'])
                    contract.append(contracttype)
                futures["bitmex"] = {
                    "contract" : contract,
                    "dates": dates,
                    "bids" : np.array(bids),
                    "asks" : np.array(asks),
                    "last" : np.array(last)
                    }
        #okcoin
    if (exchanges == None or "okcoin" in exchanges):
        symbols = []
        dates = []
        bids = []
        asks = []
        last = []
        contract = []
        for i in ["this_week", "next_week", "month", "quarter"]:
            response = requests.get('https://www.okcoin.com/api/future_ticker.do',
                                    params={"symbol": "btc_usd",
                                        "contractType":
                                            i})
            data = response.json()["ticker"][0]
            d = datetime.date(int(str(data['contractId'])[0:4]),
                              int(str(data['contractId'])[4:6]),
                              int(str(data['contractId'])[6:8]))
            dates.append(date_stamp(d))
            bids.append(data["buy"])
            asks.append(data['sell'])
            last.append(data['last'])
            contract.append("XBT")
            futures['okcoin'] = {"dates": dates,
                                 "contract" : contract,
                                 "bids" : np.array(bids),
                                 "asks" : np.array(asks),
                                 "last": np.array(last)}
    #796
    if (exchanges == None or "796" in exchanges):
        data = requests.get("http://api.796.com/v3/futures/ticker.html?type=weekly").json()['ticker']
        futures['796'] = {'dates':[date_stamp(weekly_expiry())],
                          "contract" : ["XBT"],
                          "bids" : np.array([float(data['buy'])]),
                          "asks" : np.array([float(data['sell'])]),
                          "last" : np.array([float(data['last'])])}
        data = requests.get("http://api.796.com/v3/futures/ticker.html?type=btccnyweeklyfutures").json()['ticker']
        if float(data['buy']) > 0.0 and float(data['sell']) > 0.0:
            futures['796CNY'] = {'dates':[weekly_expiry()],
                                 "bids" :
        np.array([float(data['buy'])/usdcny]),
                                 "asks" :
        np.array([float(data['sell'])/usdcny]),
                                 "last" :
        np.array([float(data['last'])/usdcny])}
    # bitvc
    if (exchanges == None or "bitvc" in exchanges):
        dates= []
        bids = []
        asks = []
        last = []
        contract = []
        for i in ["week", "next_week", "quarter"]:
            data = requests.get('http://market.bitvc.com/futures/ticker_btc_' + i + '.js').json()
            dates.append(date_stamp(expiry[i]))
            bids.append(data['buy'])
            asks.append(data['sell'])
            last.append(data['last'])
            contract.append("XBT")
        futures['bitvc'] = {'dates':dates,
                            "bids" : np.array(bids).astype(float)/usdcny,
                            "asks" : np.array(asks).astype(float)/usdcny,
                            "last" : np.array(last).astype(float)/usdcny,
                            "contract" : contract}      
    retval['futures'] = futures
    return retval

if __name__ == "__main__":
    pprint.pprint(get_data())
