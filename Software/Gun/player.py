INGAME = 1
INTEAM = 2
UP = 4 
SHIELDED = 8
ALIVE = 16
KICKED = 32


class Team:
    def __init__(self, team, player, colour, teamname):
        self.team = team
        self.player = player 
        self.colour = colour 
        self.teamname = teamname 

class Player:
    def __init__(self, playerid):
        """
        Initialises the player
        playerid: the unique id of the player
        """
        self.playerid = playerid 
        self.name = ""
        self.team = None
        self.state = ALIVE
        self.onstatechanged = None
        self.fx = None

    
    @property
    def canfire(self):
        """
        Is the player currently in a state where they can fire?
        """
        return ((self.state & INGAME) == INGAME) and ((self.state & UP) == UP) and ((self.state & ALIVE) == ALIVE) and not ((self.state & KICKED) == KICKED) 

    @property
    def canreload(self):
        """
        Is the player currently in a state where they can reload?
        """
        return ((self.state & INGAME) == INGAME) and ((self.state & UP) == UP) and ((self.state & ALIVE) == ALIVE) and not ((self.state & KICKED) == KICKED) 

    @property
    def canbehit(self):
        """
        Is the player currently in a state where they can be shot?
        """
        return ((self.state & INGAME) == INGAME) and ((self.state & INTEAM) == INTEAM) and ((self.state & UP) == UP) and ((self.state & ALIVE) == ALIVE) and not ((self.state & KICKED) == KICKED) and not ((self.state & SHIELDED) == SHIELDED) 

    def _triggerstatechange(self):
        """
        State has changed, call the onstatechange callback if set
        """
        print("player state changed, state="+str(self.state))
        self.fx.update()
        if self.onstatechanged != None:
            print("calling onstatechanged")
            self.onstatechanged(self.state)
        else:
            print("no onstatechanged callback")

    def joingame(self, game):
        """
        Join a game

        gameid: the unique identifier of the game
        """
        self.game = game
        self.state |= INGAME
        self._triggerstatechange() # trigger state change callback

    def leavegame(self):
        """
        Leave game
        """
        self.game = None
        self.state &= ~INGAME 
        self._triggerstatechange() # trigger state change callback
    
    def unassign(self):
        """
        Leave team
        """
        self.team = None
        self.state &= ~INTEAM
        self._triggerstatechange() # trigger state change callback

    def assign(self, team):
        """
        Assign this player to a team
        
        team: the Team being joined
        """
        self.team = team 
        self.state |= INTEAM
        self._triggerstatechange() # trigger state change callback

    def up(self):
        self.state |= UP
        if self.fx != None:
            self.fx.activate() 
        self._triggerstatechange() # trigger state change callback
    
    def down(self):
        self.state &= ~UP
        if self.fx != None:
            self.fx.deactivate()
        self._triggerstatechange() # trigger state change callback

    def shield(self):
        self.state |= SHIELDED
        if self.fx != None:
            self.fx.shield()
        self._triggerstatechange() # trigger state change callback
    
    def unshield(self):
        self.state &= ~SHIELDED
        if self.fx != None:
            self.fx.unshield()
        self._triggerstatechange() # trigger state change callback
    
    def kill(self):
        self.state &= ~ALIVE
        if self.fx != None:
            self.fx.deactivate()
        self._triggerstatechange() # trigger state change callback
    
    def resurrect(self):
        self.state |= ALIVE
        if self.fx != None:
            self.fx.activate()
        self._triggerstatechange() # trigger state change callback

