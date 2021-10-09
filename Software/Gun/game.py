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
# game.py
# Provides the Game class, which models the game and interacts with the
# StramashClient. New game types are implemented by subclassing Game.
# ----------------------------------------------------------------------


########################################################################
# TODO State changes should be made by the Game calling player.up etc
# ALL network comms to be handled by the Game
# TODO Free-For-All Game class
########################################################################
        
class Hit:
    """
    Represents a hit
    """

    def __init__(self, shooterteam, shooter, victimteam, victim, sensor):
        self.shooterteam = shooterteam 
        self.shooter = shooter 
        self.victimteam = victimteam 
        self.victim = victim 
        self.sensor = sensor

    @property
    def message(self):
        # TODO: hits should really only ever be JSONified in the StramashClient
        """
        Returns the JSON for the hit
        """
        msg = "["+str(self.shooterteam)+","+str(self.shooter)+","+str(self.victimteam)+","+str(self.victim)+","+str(self.sensor)+"]"
        return msg

class Game:
    """
    Base class for implementing a Game. To create a specific Game, subclass this.
    """
    def __init__(self, stramash):
        """
        Initialises the game. Subclasses should invoke this via super().__init__()
        in order to get the networking etc hooked up.
        """
        # TODO: hookup callbacks to stramash
        # TODO: kick off a thread to sleep until game end, and then call the game end code

        pass 


    ############################################################################
    # Pre Game Start
    ############################################################################
    # TODO: stramash/player/<playerid>/gamejoined - create the appropriate Game
    # object
    # TODO: stramash/player/<playerid>/assigned
    # TODO: stramash/player/<playerid>/unassigned
    # TODO: stramash/player/<playerid>/deleted
    # TODO: stramash/player/<playerid>/kicked - NOT USED IN PROTO
    # TODO: stramash/player/<playerid>/up - NOT USED IN PROTO
    # TODO: stramash/player/<playerid>/down - NOT USED IN PROTO
    # TODO: stramash/game/<gameid>/gamestarted
    #       In proto, this will shut down network
    # TODO: stramash/game/<gameid>/gamedeleted
    # TODO: 


    ############################################################################
    # During Game Play
    ############################################################################
    
    
    # TODO: Hook hit/fire callbacks - post-prototype we will send:
    # - stramash/game/<gameid>/fire
    # - stramash/game/<gameid>/hit
    # TODO: handlers for in-game network server messages. NB: we are disabling 
    # network during gameplay in the prototype to improve IR accuracy
    # TODO: stramash/game/<gameid>/gameended - NOT USED IN PROTO
    

    ############################################################################
    # Post Game Finish
    ############################################################################
    # TODO: PROTO- gun must send stats on shots fired and hits to server, and 
    # go back to initial state.
    pass