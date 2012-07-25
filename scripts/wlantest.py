#!/usr/bin/python
##
## wlantest.py
##
## Script for automatic wireless testing using hostapd
##
## Author(s):
##  - Maxence VIALLON <mviallon@aldebaran-robotics.com>
##

OUTPUT_FILE = '/home/maxence/src/wlantest/scripts/wlantest.log'
AUTO_TIMEOUT = 120

import os
from time import sleep
import ConfigParser

TEST_DIR = '/home/maxence/src/wlantest/scripts/conf'
TEST_FILES = os.listdir(TEST_DIR)

from ConnmanClient import ConnmanClient
from Hostapd import Hostapd

class wlantest:

    def __init__(self):
        self.connman = ConnmanClient()
        self.hostapd = Hostapd()

        self.output = open(OUTPUT_FILE, 'w')

    def run(self, file):
        #Reading test file
        config = ConfigParser.RawConfigParser()
        config.read(TEST_DIR + '/' + file)

        #Parsing file to dictionary
        dict = {}
        for section in config.sections():
            dict.update(config.items(section))

        #APConfig
        if dict['security'] == 'open':
            self.hostapd.open(dict['ssid'])
        elif dict['security'] == 'wep':
            self.hostapd.wep(dict['ssid'], dict['passphrase'])
        elif dict['security'] == 'wpa-psk':
            self.hostapd.wpa_psk(dict['ssid'], dict['passphrase'])
        elif dict['security'] == 'wpa2-psk':
            self.hostapd.wpa2_psk(dict['ssid'], dict['passphrase'])
        elif dict['security'] == 'wpa-eap':
            self.hostapd.wpa_eap(dict['ssid'])
            self.connman.setConfig(Name = dict['ssid'], \
                                EAP = dict['method'], \
                                Phase2 = dict['phase2'])
        elif dict['security'] == 'wpa2-eap':
            self.hostapd.wpa2_eap(dict['ssid'])
            self.connman.setConfig(Name = dict['ssid'], \
                                EAP = dict['method'], \
                                Phase2 = dict['phase2'])

        #Connecting
        if dict['type'] == 'manual':
            self.connman.scan()
            ServiceId = self.connman.getServiceId(dict['ssid'])
            if dict['security'] == 'open':
                self.connman.connect(ServiceId)
            elif dict ['security'] in ('wep', 'wpa-psk', 'wpa2-psk'):
                self.connman.connect(ServiceId, \
                                    passphrase = dict['passphrase'])
            elif dict ['security'] in ('wpa-eap', 'wpa2-eap'):
                self.connman.connect(ServiceId, \
                                    passphrase = dict['passphrase'], \
                                    identity = dict['identity'])

        elif dict['type'] == 'auto':
            ServiceId = self.connman.getServiceId(dict['ssid'])
            if dict['security'] == 'open':
                self.connman.setConfig(Name = dict['ssid'])
            elif dict ['security'] in ('wep', 'wpa-psk', 'wpa2-psk'):
                self.connman.setConfig(Name = dict['ssid'], \
                                    Passphrase = dict['passphrase'])
            elif dict ['security'] in ('wpa-eap', 'wpa2-eap'):
                self.connman.setConfig(Name = dict['ssid'], \
                                    EAP = dict['method'], \
                                    Phase2 = dict['phase2'], \
                                    Passphrase = dict['passphrase'], \
                                    Identity = dict['identity'])
            sleep(120)

        #Testing
        if self.connman.getState(ServiceId) == dict['state']:
            self.output.write('Test ' + dict['id_test'] + ' - [Ok]\n')
        else:
            self.output.write('Test ' + dict['id_test'] + ' - [Err]\n')

        #Disconnecting
        self.connman.disconnect(ServiceId)

    def stop(self):
        self.hostapd.kill()
        self.output.close()

if (__name__ == "__main__"):

    wlantest = wlantest()

    for file in TEST_FILES:
        wlantest.run(file)

    wlantest.stop()

