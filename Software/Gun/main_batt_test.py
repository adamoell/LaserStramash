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
# main.py
# Sets up the hardware and joins the game network.
# ----------------------------------------------------------------------

import time
import machine
import gc
from stramashclient import *
from player import *
from sensor import Sensor
from gun import Gun
from utils import *
from fx import *
import math

startup = time.time()

config = Config("ls.json")

# Announce the game version
ls_version = config.get('Game:version')   
header = "Laser Stramash "+ls_version
dbg(header)
dbg("-"*len(header))

# clock faster for IR
machine.freq(240000000) # default is 160000000
dbg('ESP32 running at ' + str(machine.freq()))

id = config.get('Hardware:identifier') # unique identifier for this hardware

# setup player
player = Player(id)

# setup FX
laser_pin = config.get_int('Hardware:laser_pin')
laser_brightness = config.get_int('Hardware:laser_brightness') # 0=off, 1023=max
laser = Laser(laser_pin, laser_brightness, player)

rgb_pin = config.get_int('Hardware:rgb_pin')
rgb_num_pixels = config.get_int('Hardware:rgb_num_pixels')
rgb = RGB(rgb_pin, rgb_num_pixels, player)

fx = FX()
fx.add(laser)
fx.add(rgb)
player.fx = fx

# TODO: bootup FX

# setup sensor
ir_recv_pin = config.get_int('Hardware:ir_recv_pin')
sensorid = config.get_int('Hardware:gun_sensor_id')
sensorname = config.get('Hardware:gun_sensor_name')
sensor = Sensor(ir_recv_pin, sensorid, sensorname, player, fx, True)

# setup gun
dbg('Initialising gun...')
fire_pin = config.get_int('Hardware:fire_pin')
reload_pin = config.get_int('Hardware:reload_pin')
ir_send_pin = config.get_int('Hardware:ir_send_pin')
max_ammo = 10 # should get overridden by game
reload_time = 5 # should get overridden by game
gun = Gun(fire_pin, reload_pin, ir_send_pin, fx, player, max_ammo, reload_time)

dbg('Connecting to server...')
wifi_ssid = config.get('Network:wifi_ssid')
wifi_key = config.get('Network:wifi_key')
server_address = config.get('Network:mqtt_server_address')
stramash = StramashClient(id, server_address, wifi_ssid, wifi_key)
# TODO: hook ongamejoined callback from stramash client and use it to 
# 'save' the game and populate its gun, sensor, player

###############################################################################
# TEST CODE this stuff should really be done by a Game
###############################################################################
testteam = Team(1, 1, (192, 192, 255), "Test Team")
testgame = "Test Game" # TODO this should be a Game object!

# #player.onstatechanged = rgb.handlestatechange # let the RGB update when player state changes
player.assign(testteam)
player.joingame(testgame)
player.up()
# # TODO player.joingame --> gun, sensor
# # Game hooks sensor.onhit - mark player and gun as dead
# # ie game logic... probably reload, can_fire, can_reload handled here...
# # TODO game needs to maintain a list of enemy teams VALIDATED by the Fire method
# # when the game starts, turn off WiFi.

###############################################################################
# event loop
print('Starting Event Loop')
cycles = 0
firecounter = 0
reloadcounter = 0
reloadstart = -100

try:
    while True:
        now = time.time()
        runtime = time.time() - startup
        m, s = divmod(runtime, 60)
        h, m = divmod(m, 60)
        
        # fire every second
        # don't fire if reloaded < 6 sec ago
        if (now - reloadstart) >= 6:
            fx.fire()
            firecounter += 1

        cycles += 1
        uptime = 'Up for {:d} secs ({:02d}:{:02d}:{:02d}) - {:d} shots fired, {:d} reloads'.format(runtime,h,m,s, firecounter, reloadcounter)
        print(uptime)
        stramash.send('status', uptime)

        # reload every 10 seconds
        if runtime % 15 == 0:
            reloadstart =  now
            fx.reload()
            #sleep(5)
            reloadcounter += 1 
        
        stramash.update() # TODO can we schedule this with a thread in the StramashClient?
        
        time.sleep(1)
        gc.collect()
except KeyboardInterrupt:
    sensor.close()
    fx.close()