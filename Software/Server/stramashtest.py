# stramashtest.py 

import unittest
from stramash import *

class StramashTests(unittest.TestCase):
    # --------------------------------------------------------------------------
    # COLOUR TESTS
    # --------------------------------------------------------------------------
    def test_colour_create(self):
        red = Colour("Red", 255, 0, 0)
        self.assertEqual(red.name, "Red")
        self.assertEqual(red.red, 255)
        self.assertEqual(red.green, 0)
        self.assertEqual(red.blue, 0)

        with self.assertRaises(TypeError):
            red = Colour(0,0,0,0)
            red = Colour("Red","0",0,0)
            red = Colour("Red",0,"0",0)
            red = Colour("Red",0,0,"0")

    def test_colour_serialisation(self):
        # create a colour, serialise, make sure the serialisation is as expected 
        red = Colour("Red", 255, 0, 0)
        expected = '["Red",255,0,0]'
        self.assertEqual(red.serialise(), expected)

    def test_colour_deserialisation(self):
        # deserialise from string, ensure properties as expected
        redserial = '["Red",255,0,0]'
        greenserial = '["Green",0,255,0]'
        blueserial = '["Blue",0,0,255]'
        red = Colour.deserialise(redserial)
        green = Colour.deserialise(greenserial)
        blue = Colour.deserialise(blueserial)
        self.assertEqual(red.name, "Red")
        self.assertEqual(red.red, 255)
        self.assertEqual(red.green, 0)
        self.assertEqual(red.blue, 0)
        self.assertEqual(green.name, "Green")
        self.assertEqual(green.red, 0)
        self.assertEqual(green.green, 255)
        self.assertEqual(green.blue, 0)
        self.assertEqual(blue.name, "Blue")
        self.assertEqual(blue.red, 0)
        self.assertEqual(blue.green, 0)
        self.assertEqual(blue.blue, 255)

        # make sure it doesn't allow invalid colours
        bad1 = '["Test",-1,0,0]'
        bad2 = '["Test",255,0,0]'
        bad3 = '["Test",0,-1,0]'
        bad4 = '["Test",0,255,0]'
        bad5 = '["Test",0,0,-1]'
        bad6 = '["Test",0,0,255]'
        with self.assertRaises(ColourOutOfRange):
            clr = Colour.deserialise(bad1)
            clr = Colour.deserialise(bad2)
            clr = Colour.deserialise(bad3)
            clr = Colour.deserialise(bad4)
            clr = Colour.deserialise(bad5)
            clr = Colour.deserialise(bad6)
    


    # --------------------------------------------------------------------------
    # PLAYER TESTS
    # --------------------------------------------------------------------------
    def test_player_create(self):
        # TODO: create a team, test properties
        # Properties
        # name
        # id
        # team
        # colour
        # shots (int)
        # kills (int)
        # deaths (int)
        # score (int)
        player = Player(1, "Adam")
        self.assertEqual(1, 2)

    # def test_player_serialisation(self):
    #     # TODO: create a player, serialise, make sure the serialisation is as expected 
    #     self.assertEqual(1, 2)

    # def test_player_deserialisation(self):
    #     # TODO: deserialise from string, ensure properties as expected
    #     self.assertEqual(1, 2)

    # def test_player_handle_fire(self):
    #     # TODO invoke handle_fire and ensure shots is incremented
    #     self.assertEqual(1, 2) 

    # def test_player_handle_kill(self):
    #     # TODO invoke handle_kill and ensure kills is incremented
    #     self.assertEqual(1, 2) 
    #     # TODO handle_kill with invalid killer id and ensure exception

    # def test_player_handle_death(self):
    #     # TODO invoke handle_death and ensure deaths is incremented
    #     self.assertEqual(1, 2) 

    # # --------------------------------------------------------------------------
    # # TEAM TESTS
    # # --------------------------------------------------------------------------
    # def test_team_create(self):
    #     # TODO: create a team, test properties
    #     # Properties:
    #     # name
    #     # id
    #     # players
    #     self.assertEqual(1, 2)

    # def test_team_serialisation(self):
    #     # TODO: create a team, serialise, make sure the serialisation is as expected 
    #     self.assertEqual(1, 2)

    # def test_team_deserialisation(self):
    #     # TODO: deserialise from string, ensure properties as expected
    #     self.assertEqual(1, 2)

    # def test_team_addplayer(self):
    #     # TODO: create team, create player, add player to team, test
    #     self.assertEqual(1, 2)

    # def test_team_deleteplayer(self):
    #     # TO: create team, create player, add player to team, delete player, ensure not there 
    #     self.assertEqual(1, 2)

    # # --------------------------------------------------------------------------
    # # GAME TESTS
    # # --------------------------------------------------------------------------
    # def test_game_create(self):
    #     # TODO: create a game, test properties
    #     # properties:
    #     # name
    #     # start_time
    #     # players
    #     # teams
    #     # state: 0=Unstarted, 1=Active, 2=Finished
    #     self.assertEqual(1, 2)

    # def test_game_addteam(self):
    #     # TODO: create game, create team, add team to game, test
    #     self.assertEqual(1, 2)

    # def test_game_deleteteam(self):
    #     # TODO: create game, create team, add team to game, delete team, ensure not there 
    #     self.assertEqual(1, 2)

    # def test_game_addplayer(self):
    #     # TODO: create game, create player, add player to game, test
    #     self.assertEqual(1, 2)

    # def test_game_deleteplayer(self):
    #     # TODO: create game, create player, add player to game, delete player, ensure not there 
    #     self.assertEqual(1, 2)

    # def test_game_serialisation(self):
    #     # TODO: create a game, add teams, add players, serialise it, make sure the serialisation is as expected
    #     self.assertEqual(1, 2)

    # def test_game_deserialisation(self):
    #     # TODO: create a game, add teams, add players, serialise it, make sure the serialisation is as expected
    #     self.assertEqual(1, 2)

    # def test_game_saveload(self):
    #     # TODO: create a game, add teams, add players, save it, load it, test it
    #     self.assertEqual(1, 2)

    
if __name__ == '__main__':
    unittest.main()