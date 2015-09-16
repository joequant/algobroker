#!/usr/bin/env python3

from flask import Flask, send_from_directory
import algobroker
import flask
from io import StringIO
import sys
app = Flask(__name__, static_url_path='')

@app.route("/")
def hello():
    return app.send_static_file('controller_hello.html')

@app.route("/test-data")
def testdata():
    return flask.jsonify({"records" : [{"Name" : "foo",
                           "Country" : "bar"},
                          {"Name" : "foo1",
                           "Country" : "bar1"}]})

@app.route("/desk-alert")
def deskalert():
    algobroker.send("data",
                    [{"dest" : "broker_desk_alert",
                     "cmd" : "alert",
                     "type" : "desk",
                     "alert" : "high"}])
    return "alert"

if __name__ == "__main__":
    app.run(debug=True)
