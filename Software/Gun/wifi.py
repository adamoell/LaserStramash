# Laser Stramash: weapons-grade Free Software laser tag system.
# Copyright (C) 2021 Adam Oellermann
# adam@oellermann.com
# ----------------------------------------------------------------------
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------
# wifi.py
# deal with network connectivity
# ----------------------------------------------------------------------

# listen on pc:
# mosquitto_sub -h 192.168.1.2 -t dbg -t hit
from time import sleep 
import machine
import network
from utils import *

class WiFi:
    def __init__(self, ssid, key):
        self.ssid = ssid 
        self.key = key

    def connect(self):
        """
        Connect to the wifi access point
        """
        self.sta_if = network.WLAN(network.STA_IF)
        self.sta_if.active(False)
        sleep(1)
        self.sta_if.active(True)

        print("Interface active")
        if self.check_ap(self.ssid):
            # connect to access point
            if not self.sta_if.isconnected():
                print('connecting to AP...')
                self.sta_if.active(True)
                self.sta_if.connect(self.ssid, self.key)
                while not self.sta_if.isconnected():
                    machine.idle()
                    # Do we need a timeout here?
                print(self.sta_if.ifconfig())
            else:
                print("WLAN already connected")
                print(self.sta_if.ifconfig())
        else:
            print("Target SSID not found.")
            reset("Could not connect to network - target SSID is not availble.", HARD)
    
    def check_ap(self, targetssid):
        """
        Check if the given access point exists
        """
        print("Scanning for access point ["+targetssid+"]...")
        
        self.sta_if.active(True)
        networks = self.sta_if.scan()

        for ssid, bssid, channel, rssi, authmode, hidden in sorted(networks, key=lambda x: x[3], reverse=True):
            ssid = ssid.decode('utf-8')
            if ssid == targetssid:
                print("Found access point!")
                return True 
        
        print("Access point not found")
        return False


