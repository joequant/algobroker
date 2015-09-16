#!/usr/bin/python3
# Copyright (C) 2015 Bitquant Research Laboratories (Asia) Limited
# Released under the Simplified BSD License

import my_path
import pprint
import algobroker
from algobroker import Broker
import pyglet
import os

class BrokerDeskAlert(Broker):
    def __init__(self):
        Broker.__init__(self, "broker_desk_alert")
        my_dir = os.path.dirname(os.path.realpath(__file__))
        self.media_dir = os.path.join(my_dir, "media")
        self.alerts = ["low", "high"]
    def alert(self, alert):
        sound = pyglet.media.load(os.path.join(self.media_dir,
                                               alert + ".ogg"))
        sound.play()
    def process_data(self, data):
        if (data['cmd'] == "alert" and \
            data['type'] == 'desk'):
            if (data['alert'] in self.alerts):
                self.alert(data['alert'])
    def process_control(self, data):
        algobroker.Broker.process_control(self, data)

if __name__ == "__main__":
    bp = BrokerDeskAlert()
    bp.alert("high")
