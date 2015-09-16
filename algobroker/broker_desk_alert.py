#!/usr/bin/python3
# Copyright (C) 2015 Bitquant Research Laboratories (Asia) Limited
# Released under the Simplified BSD License

import my_path
import pprint
import algobroker
from algobroker import Broker
import os
import subprocess

def is_exe(fpath):
    return os.path.exists(fpath) and os.access(fpath, os.X_OK)

class BrokerDeskAlert(Broker):
    def __init__(self):
        Broker.__init__(self, "broker_desk_alert")
        my_dir = os.path.dirname(os.path.realpath(__file__))
        self.media_dir = os.path.join(my_dir, "static")
        self.alerts = ["low", "high"]
        self.repeat = 5
        self.player = "/bin/play"
    def alert(self, alert):
        if not is_exe("/bin/play"):
            print("sox not installed")
        else:
            for i in range(self.repeat):
                subprocess.call(["/bin/play", "-q",
                                 os.path.join(self.media_dir,
                                              alert + ".ogg")])
    def process_data(self, data):
        if (data['cmd'] == "alert" and \
            data['type'] == 'desk'):
            if (data['alert'] in self.alerts):
                self.alert(data['alert'])
    def process_control(self, data):
        algobroker.Broker.process_control(self, data)

if __name__ == "__main__":
    bp = BrokerDeskAlert()
    bp.run()

