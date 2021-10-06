# Laser Stramash: the openest, coolest laser tag system
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
# sensor.py
# provides the class Sensor, which deals with receiving infrared.
# ----------------------------------------------------------------------
# Currently relies on Peter Hinch's IR library:
# https://github.com/peterhinch/micropython_ir/blob/master/RECEIVER.md
#
# though probably this will move onto separate hardware (eg ATtiny85) soon,
# as the code recognition is a bit unstable when the ESP32 is doing other 
# things. See:
# https://github.com/fotisl/ir2i2c
# Have a wee look at comment here: https://github.com/fotisl/ir2i2c/issues/1
# re. a more efficient version happy at 8mHz

import time
from machine import Pin, freq
from ir_rx.print_error import print_error  # Optional print of error codes
from ir_rx.nec import NEC_8, NEC_16
from game import Hit
from utils import inttohexstring



def neccode(addr, data):
    return inttohexstring(addr)+":"+inttohexstring(data)

class Sensor:
    def __init__(self, pin, sensorid, sensorname, player, fx, excludefriendly=True):
        """
        Setup the sensor. Raises callbacks: onhit, onfriendlyfire if these
        are assigned

        pin: the GPIO pin number of the IR sensor
        sensorid: the id of the sensor
        sensorname: the name of this sensor
        player: the player
        excludefriendly: if True, exclude friendly fire
        onhit: optional callback to invoke when a hit is verified
        """
        # initialise IR receiver
        ir_recv_pin = Pin(pin, Pin.IN)
        self.ir = NEC_8(ir_recv_pin, self.handle_ir)  # Instantiate receiver
        self.sensorid = sensorid
        self.sensorname = sensorname
        self.player = player
        self.excludefriendly = excludefriendly
        self.onhit = None
        self.onfriendlyfire = None
        self.hits = []
        self.fx = fx

    # handle received IR code
    def handle_ir(self, data, addr, ctrl): 
        if data > 0: # ignore repeat codes
                
            if self.player.canbehit: # can we be hit? IE not shielded, dead etc
                myteam = self.player.team.team
                myplayer = self.player.team.player

                hit = Hit(addr, data, myteam, myplayer, self.sensorid)
                friendlyfire = (addr == myteam)
                if (not friendlyfire) or (not self.excludefriendly): # no friendly fire!
                    self.hits.append(hit)
                    print("hit: counter=" + str(len(self.hits)))
                    self.fx.hit()
                    if self.onhit != None:
                        self.onhit(hit)
                else:
                    # Deal with friendly fire here if needed - but only if this wasn't me shooting myself!
                    if myplayer != data:
                        if self.onfriendlyfire != None:
                            self.onfriendlyfire(hit)
                        print("hit: not counting friendly fire")
            else:
                # deal with unhittable player if needed
                print("hit: not hittable, state="+str(self.player.state))
            
            
    def close(self):
        self.ir.close()


