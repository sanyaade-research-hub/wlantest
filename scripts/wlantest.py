#!/usr/bin/python
##
## wlantest.py
##
## Script for automatic wireless testing using hostapd
##
## Author(s):
##  - Maxence VIALLON <mviallon@aldebaran-robotics.com>
##

import os
import threading
from time import sleep

from ConnmanClient import ConnmanClient
from Hostapd import Hostapd

class AgentThread (threading.Thread):

    def __init__(self, daemon):
        threading.Thread.__init__(self)
        self.daemon = daemon


    def run(self):
        # TODO : Agent main loop
        pass

class wlantest:

    def __init__(self):
        self.connman = ConnmanClient()
        self.hostapd = Hostapd()
        self.agent = AgentThread(True)

        self.agent.start()
    
    def wpa2(self):
        self.hostapd.reload("wpa2.conf")
        print("Hostap running mode wpa2")
        
        print("Scanning wifi ...")
        self.connman.scan()
         
        # Delay for connman to autoconnect
        sleep(5)
         
        ServiceId = self.connman.getServiceId("wpa2rezo")
        if self.connman.serviceisConnected(ServiceId):
            print "Success"
        else:
            print "Fail"

    def stop(self):
        self.hostapd.kill()

if (__name__ == "__main__"):
    
    # TODO : Start dhcp
    
    wlantest = wlantest()

    wlantest.wpa2()

    wlantest.stop()

