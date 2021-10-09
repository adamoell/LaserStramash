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
# stramashclient.py
# deals with the Stramash network protocol.
# ----------------------------------------------------------------------

# MQTT testing...
# Subscribe to all:
# mosquitto_sub -h 192.168.1.2 -t "#" -v
# Send a message:
# mosquitto_pub -h 192.168.1.2 -t <topic> -m <message>
from wifi import WiFi
from umqttsimple import *
from game import Hit
from utils import *

class StramashProtocolError(Exception):
    """
    Exception raised when we receive server messages we don't understand.
    """
    pass

class StramashClient:
    """
    Network protocol handler.
    """
    def __init__(self, playerid, server, wifi_ssid, wifi_key):
        """
        Sets up the client, connects to wifi and establishes the connection to 
        the MQTT server.

        playerid: unique identifier for this client
        server: address of the MQTT broker
        wifi_ssid: SSID of the WiFi network
        wifi_key: PSK for the WiFi network
        """

        self.playerid = playerid
        self.game = None # will get set when we get joined
        self.onmessage = None # message handler for MQTT messages received

        # print("Connecting to WiFi...")
        # self.wifi = WiFi(wifi_ssid, wifi_key)
        # self.wifi.connect()
        # print("WiFi connected")
    
        # self.mqtt_client = MQTTClient(playerid, server)
        # self.mqtt_client.set_callback(self.receive)
        # self.mqtt_client.connect()
        # # TODO .connect(clean_session=False) ? 
        # # https://www.hivemq.com/blog/mqtt-essentials-part-7-persistent-session-queuing-messages/
        # # maybe just on reconnect?
        # print('MQTT connected')

        self.mqtt_client = None
        print('MQTT not connected')

        # setup a dictionary of topics and their handler methods 
        self.topic_handlers = {
            "stramash/player/"+self.playerid+"/gamejoined": self._gamejoined,
            "stramash/player/"+self.playerid+"/assigned": self._assigned,
            "stramash/player/"+self.playerid+"/unassigned": self._unassigned,
            "stramash/player/"+self.playerid+"/deleted": self._deleted,
            "stramash/player/"+self.playerid+"/kicked": self._kicked,
            "stramash/player/"+self.playerid+"/up": self._up,
            "stramash/player/"+self.playerid+"/down": self._down
        }
        # Note: we can't add gamestarted, gameended and gamedeleted because
        # we won't know their topics until we have a game ID
        
        # subscribe to the topics
        for topic in self.topic_handlers.keys():
            self.subscribe(topic)
        
        # blank all the event handlers
        self.ongamejoined = None
        self.onassigned = None
        self.onunassigned = None
        self.ondeleted = None
        self.onkicked = None
        self.onup = None
        self.ondown = None

        self.ongamestarted = None
        self.ongameended = None
        self.ongamedeleted = None

    def subscribe(self, topic):
        """
        Subscribes to the specified MQTT topic.

        topic: the topic to subscribe to.
        """
        if self.mqtt_client != None:
            self.mqtt_client.subscribe(topic) # subscribe to hit messages

    def receive(self, topic, msg):
        """
        Receives a message from the network, and invokes the appropriate 
        handler code.

        topic: MQTT topic
        msg: MQTT message
        """
        topic = topic.decode('utf-8')
        msg = msg.decode('utf-8')
        dbg('From MQTT: ' + topic + ":" + msg)
        
        # generic message handler
        if self.onmessage != None:
            self.onmessage(topic, msg)
        
        # call the code to deal with the message
        if topic in self.topic_handlers:
            handler = self.topic_handlers[topic]
            handler(topic, msg)
        else:
            # Invalid message - log, raise exception
            dbg("Unexpected topic received from server")
            raise StramashProtocolError("An unexpected topic was received from the server.")
            


    def send(self, topic, msg):
        """
        Publishes an MQTT message. This should ONLY be called by StramashClient
        methods.

        topic: the topic to publish
        msg: the message
        """
        if self.mqtt_client != None:
            self.mqtt_client.publish(topic, msg)
            #print('> To MQTT: ' + topic + ":" + msg)

    def update(self):
        """
        Needs to be called periodically to obtain queued messages from the server.
        
        TODO: this is currently run in the main loop, but it would be much neater
        to simply run it in a thread.
        """
        if self.mqtt_client != None:
            self.mqtt_client.check_msg()

    def sendfire(self):
        """
        Tell the server we have fired.
        """
        # NB: This is not used in the prototype. 
        # TODO: Might be better to send the /total/ fired each time?
        topic = "stramash/"+self.game.id+"/fire"
        self.send(topic, self.playerid)
        

    def sendhit(self, hit):
        """
        Tell the server we have been hit.
        """
        # NB: this is not used in the prototype.
        # send hit message to the server
        topic = "stramash/game/"+self.game.id+"/hit"
        self.send(topic, hit.message)
        


            
    ############################################################################
    # Implement Actions for Server Messages: Pre Game Start
    ############################################################################
    def _gamejoined(self, topic, msg):
        print("stramashclient: _gamejoined")
        # TODO: stramash/player/<playerid>/gamejoined - create the appropriate Game
        # object and feed it gun, fx, player
        
        # TODO: set these topic names and subscribe to them
        # TODO append to self.topic_handlers 
        # self.topic_handlers["topic"] = self._gamestarted
        #self.topic_gamestarted = ""
        #self.topic_gameended = ""
        #self.topic_gamedeleted = ""

        # TODO send the Game to ongamejoined callback
        

    def _assigned(self, topic, msg):
        print("stramashclient: _assigned")
        # TODO: stramash/player/<playerid>/assigned
        # TODO create Team object 
        # TODO player.assign(..)
        # TODO send the team, player to onassigned callback
    
    def _unassigned(self, topic, msg):
        print("stramashclient: _unassigned")
        # TODO: stramash/player/<playerid>/assigned
        # TODO null None object
        # TODO player.unassign(..)
        # TODO send the  player to onunassigned callback

    def _deleted(self, topic, msg):
        print("_deleted")
        # TODO FX
        reset("Player Deleted", HARD)
    
    def _kicked(self, topic, msg):
        print("_kicked")
        # TODO FX
        reset("Kicked by Server", HARD)

    def _gamedeleted(self, topic, msg):
        print("_kicked")
        # TODO FX
        reset("Game Deleted")

    def _gamestarted(self, topic, msg):
        print("_gamestarted")
        # TODO: PROTO: turn off network, start game timer, player "up"


    ############################################################################
    # During Game Play
    ############################################################################
    # TODO: Hook hit/fire callbacks - post-prototype we will send:
    # - stramash/game/<gameid>/fire
    # - stramash/game/<gameid>/hit
    
    def _up(self, topic, msg):
        print("_up")
        # NOT USED IN PROTOTYPE - no network during game

    def _down(self, topic, msg):
        print("_down")
        # NOT USED IN PROTOTYPE - no network during game

    def _gameended(self, topic, msg):
        print("_gameended")
        # TODO: in prototype, this is not actually a server message
        # but is invoked by the timer thread.
        # Post-prototype, this will ONLY be invoked via a server message.
        # TODO PROTO: Reconnect network and transmit stats.
        
        # Then reset...
        # TODO Game Over FX
        reset("Game Ended", HARD)