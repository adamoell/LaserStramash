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
# stramash.py
# Implements the Laser Stramash server
# ----------------------------------------------------------------------
import json
import game
from utils import *
from game import *
from player import *
from team import *
from colour import *
import paho.mqtt.client as mqtt

games = {}

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("stramash/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global games

    print(msg.topic+" "+str(msg.payload))
    # TODO dispatch the message to the game or whatever...
    topic = str(msg.topic)
    data = str(msg.payload.decode("utf-8", "ignore"))
    if topic == "stramash/newgame":
        

        


def welcome():
    print('================================================================================')
    print('Laser Stramash - Prototype')
    print('Game Server')
    print('================================================================================')

# initialise config
config = Config("server.json")

# Get started
welcome() 

# Connect to MQTT broker 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
mqtt_broker = config.get("Network:mqtt_server_address")
client.connect(mqtt_broker, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()


