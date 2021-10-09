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
# gun.py
# provides the Gun class
# ----------------------------------------------------------------------

from machine import Pin, PWM, Timer
from player import *
from buttons import *
from time import sleep
import _thread
from fx import *
from ir_tx.nec import NEC


class Gun:
    """
    Encapsulates a Gun and its hardware (buttons, laser, infrared emitter)
    """
    def __init__(self, fire_pin, reload_pin, ir_send_pin, fx, player, max_ammo, reload_time):
        """
        Initialise the gun.
        fire_pin: the GPIO for the fire button
        reload_pin: the GPIO for the reload button
        ir_send_pin: the GPIO for the IR LED
        fx: the FX object
        player: the player object
        max_ammo: the maximum amount of ammo the player can hold
        """
        self.game = None
        self.team = None
        self.player = player
        self.firecounter = 0
        self.reloadcounter = 0
        self.max_ammo = max_ammo
        self.ammo = max_ammo
        self.reloading = False
        self.reload_time = reload_time
        self.fx = fx

        self.onfire = None # set this to get called back when the fire button is pressed
        self.onreload = None # set this to get called back when the reload button is pressed
        self.onoutofammo = None # set this to get called back when the gun is out of ammo

        # configure hardware
        self.activate_buttons(fire_pin, reload_pin)
        self.activate_ir(ir_send_pin)        


    def activate_buttons(self, fire_pin, reload_pin):
        """
        Activates the fire and reload pins and their callbacks

        fire_pin: GPIO for the fire button
        reload_pin: GPIO for the reload button
        """
        
        # fire button
        self.fire_pin = fire_pin
        fire = Pin(fire_pin, Pin.IN, Pin.PULL_UP)
        self.fire_button = DebouncedSwitch(fire, self._fire, arg=None) # arg is sent to the callback
        
        # reload button
        self.reload_pin = reload_pin
        reload = Pin(reload_pin, Pin.IN, Pin.PULL_UP)
        self.reload_button = DebouncedSwitch(reload, self._reload, arg=None) # arg is sent to the callback

    def activate_ir(self, ir_send_pin):
        """
        Configures the IR transmitter

        ir_send_pin: the pin to use for ir transmission
        """
        self.ir_send_pin = ir_send_pin 
        ir = Pin(ir_send_pin, Pin.OUT, value=0)
        self.ir_sender = NEC(ir)


    def send_ir(self, addr, data):
        """
        Sends an NEC protocol command

        addr: the address (0-255) - represents the team
        data: the command (0-255) - represents the player
        """
        self.ir_sender.transmit(addr, data)

    def _fire(self, arg=None):
        """ 
        Event handler for when the Fire button is pressed
        """
        # are we allowed to fire?
        if self.player.canfire:
            if not self.reloading:
                # do we have ammo?
                if self.ammo > 0:
                    self.firecounter += 1
                    self.ammo -= 1
                    print("fire: shots fired="+str(self.firecounter)+"; ammo left="+str(self.ammo))
                    myteam = self.player.team.team
                    myplayer = self.player.team.player
                    self.send_ir(myteam, myplayer)
                    
                    self.fx.fire() # special effects - laser and RGB
                    
                    if self.onfire != None: # optional callback
                        self.onfire
                else:
                    print("fire: no ammo")
                    self.fx.firefail()
                    # out-of ammo callback
                    if self.onoutofammo != None:
                        self.onoutofammo
            else: 
                print("fire: reloading")
        else:
            print("fire: not allowed, state="+str(self.player.state))

    def _reload_activate(self):
        """
        Thread method that waits for the reload time, the reactivates the gun
        and tops up the ammo.
        """
        time.sleep(self.reload_time)
        self.reloading = False 
        self.ammo = self.max_ammo
        dbg("reload: complete, ammo="+str(self.ammo))

        if self.onreloadcomplete != None: # optional callback
            self.onreloadcomplete

    def _reload(self, arg=None):
        """ 
        Event handler for when the Reload button is pressed
        """

        # are we allowed to reload?
        if self.player.canfire:
            if not self.reloading:
                print("reload: starting...")
                self.reloading = True
                _thread.start_new_thread(self._reload_activate, ())
                
                self.fx.reload() # handle the SFX
                if self.onreload != None: # optional callback
                    self.onreload

            else:
                print("reload: already busy reloading")
        else:
            print("reload: not allowed, state="+str(self.player.state))


