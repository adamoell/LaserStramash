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
# launcher.py
# Simple interactive command-line app to get a game launched.
# ----------------------------------------------------------------------

import os, random

game_ready = False 
teams_ready = False 
players_ready = False 
launched = False

def unique_id(length=8):
    """
    Generates a random unique identifier.
    """
    #alphabet = string.ascii_letters + digits
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz01234567890"
    return ''.join(random.choices(alphabet, k=length))

colours = {
    "Red": "[255,0,0]",
    "Orange": "[255,128,0]",
    "Yellow": "[255,255,0]",
    "Green": "[0,255,0]",
    "Blue": "[0,0,255]",
    "Purple": "[255,0,255]",
    "Pink": "[255,128,255]"
}

class Game:
    def __init__(self):
        self.name = ""
        self.type = ""
        self.maxtime = ""
        self.gameid = ""

class Team:
    def __init__(self) :
        self.name = ""
        self.colour = ""
        self.teamid = unique_id()
        self.teamnumber = "" # IR code

class Player:
    def __init__(self):
        self.name = ""
        self.colour = ""
        self.team = None
        self.playerid = ""
        self.gunid = ""
        self.playernumber = "" # IR code

game = Game()
teams = {}
players = {}

def cls():
    os.system('clear')

def summary():
    global game_ready, teams_ready, players_ready, launched
    global game, teams, players

    if game_ready:
        print("Game Name: [{0}] Type: [{1}] Time: [{2}]".format(game.name, game.type, game.maxtime))
    if teams_ready:
        print("Teams:")
        for key, team in teams.items():
            print("-- Team: [{0}] Colour: [{1}] ID: [{2}]".format(team.name, team.colour, key))
    if players_ready:
        print("TODO Players")
    

def get_value(prompt, default):
    val = input(prompt)
    if val == "":
        val = default 
    return val 

def get_game():
    global game_ready, teams_ready, players_ready, launched
    global game, teams, players

    cls()
    print("--------------------------------------------------------------------------------")
    print("Game Setup")
    print("--------------------------------------------------------------------------------")
    print("Please enter the following data. If there is a current value, it appears in")
    print("[square brackets], and just pressing Enter will keep it.")
    print()
    game.name = get_value("Game name [{0}]: ".format(game.name), game.name)
    game.type = get_value("Game type (ffa|teams|royale) [{0}]: ".format(game.type), game.type)
    game.maxtime = get_value("Game timeout (hh:mm:ss) [{0}]: ".format(game.maxtime), game.maxtime)
    
    game_ready = True

def pick_player():
    # prompt to select a player, and then return it
    global game, teams, players
    
    lookup = {}
    playerno = 1
    for key, player in players.items():
        lookup[playerno] = player
        print("{0}: {1} - {2}".format(playerno, player.name, player.team.name))
        playerno += 1
    
    print()
    choice = int(input("Select a player: > "))
    if (choice in lookup):
        return lookup[choice]
    else:
        return None

def edit_player_values(player):
    pass 

def delete_player(): # TODO
    # add a new team
    global teams
    
    cls()
    print("Delete Team")
    print("--------------------------------------------------------------------------------")
    del_team = pick_team()
    del teams[del_team.teamid]

def edit_player(): # TODO
    # add a new team
    global teams
    
    cls()
    print("Edit Team")
    print("--------------------------------------------------------------------------------")
    edit_team = pick_team()
    edit_team_values(edit_team)

def add_player(): # TODO
    # add a new player
    global teams
    
    cls()
    print("Add New Team")
    print("--------------------------------------------------------------------------------")
    new_team = Team()
    edit_team_values(new_team)
    teams[new_team.teamid] = new_team

def pick_team():
    # prompt to select a team, and then return it
    global game, teams, players
    
    lookup = {}
    teamno = 1
    for key, team in teams.items():
        lookup[teamno] = team
        print("{0}: {1} - {2}".format(teamno, team.name, team.colour))
        teamno += 1
    
    print()
    choice = int(input("Select a team: > "))
    if (choice in lookup):
        return lookup[choice]
    else:
        return None

def edit_team_values(team):
    team.name = get_value("Name [{0}] > ".format(team.name), team.name)
    # TODO colour enumeration
    cols = ""
    for c in colours:
        cols += c + " "
    print("Available Colours: [{0}]".format(cols))
    team.colour = get_value("Colour [{0}] > ".format(team.colour), team.colour)


def delete_team():
    # add a new team
    global teams
    
    cls()
    print("Delete Team")
    print("--------------------------------------------------------------------------------")
    del_team = pick_team()
    del teams[del_team.teamid]

def edit_team():
    # add a new team
    global teams
    
    cls()
    print("Edit Team")
    print("--------------------------------------------------------------------------------")
    edit_team = pick_team()
    edit_team_values(edit_team)

def add_team():
    # add a new team
    global teams
    
    cls()
    print("Add New Team")
    print("--------------------------------------------------------------------------------")
    new_team = Team()
    edit_team_values(new_team)
    teams[new_team.teamid] = new_team

def get_teams():
    global game_ready, teams_ready, players_ready, launched
    global game, teams, players

    teams_finished = False
    while not teams_finished:
        cls()
        print("--------------------------------------------------------------------------------")
        print("Team Setup")
        print("--------------------------------------------------------------------------------")
        print("Current Teams:")
        for key, team in teams.items():
            print("Team: [{0}] Colour: [{1}] ID: [{2}]".format(team.name, team.colour, key))
        print("--------------------------------------------------------------------------------")
        print("Options:")
        print()
        print("1. Add Team")
        print("2. Edit Team")
        print("3. Delete Team")
        print("4. Return to Main Menu")

        option = input("Select an option: > ")
        if option == "1": add_team()
        if option == "2": edit_team()
        if option == "3": delete_team()
        if option == "4": teams_finished = True




    print("get_teams")
    teams_ready = True

def get_players():
    global game_ready, teams_ready, players_ready, launched
    global game, teams, players
    print("get_players")
    players_ready = True

def launch_game():
    global game_ready, teams_ready, players_ready, launched
    
    print("Launching Game!")
    launched = True


def menu():
    cls()

    global game_ready, teams_ready, players_ready, launched

    
    launched = False

    while not launched: 
        launch = {}
        menu = []

        print('================================================================================')
        print('Laser Stramash - Prototype')
        print('Game Launcher')
        print('================================================================================')
        summary()
        print('================================================================================')
        print()
        print('Main Menu')
        print('---------')
        edit_game = '1. Edit Game Parameters'
        if not game_ready:
            edit_game += ' (TODO)'
        launch['1'] = get_game
        menu.append(edit_game)

        edit_teams = '2. Edit Teams'
        if not teams_ready:
            edit_teams += ' (TODO)'
        launch['2'] = get_teams
        menu.append(edit_teams)

        edit_players = '3. Edit Players'
        if not players_ready:
            edit_players += ' (TODO)'
        launch['3'] = get_players
        menu.append(edit_players)

        if game_ready and teams_ready and players_ready:
            launch_game_text = '4. Launch Game'
            launch['4'] = launch_game
        else:
            launch_game_text = 'You cannot launch the game until all TODOs are resolved.'
        menu.append(launch_game_text)
        
        for option in menu:
            print(option)
        
        print()
        option = input("Please enter your choice: > ")
        launch[option]()

        cls()

def farewell():
    print('================================================================================')
    print('Thank you for playing the Laser Stramash Prototype!')
    print('================================================================================')

menu()
farewell()

