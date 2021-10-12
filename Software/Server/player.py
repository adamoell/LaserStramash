class Player:    
    # id
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, id):
        if not isinstance(id, int):
            raise TypeError
        self._id = id
    
    # name
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError
        self._name = name

    # colour
    @property
    def colour(self):
        return self._colour
    @colour.setter
    def colour(self, colour):
        colourOK = (colour == None) or (isinstance(colour, Colour))
        if not colourOK:
            raise TypeError
        self._name = colour

    def __init__(self, id, name, teamnumber, playernumber):
        self.id = id
        self.name = name 
        self.teamnumber = teamnumber 
        self.playernumber = playernumber
        self.colour = None 
        self.shots = 0
        self.kills = 0
        self.ffkills = 0
        self.deaths = 0
        self.score = 0
        # TODO initial status

    # TODO properties
    # id - a GUID (unique to each gun)
    # name    
    # teamnumber (0-255) used for IR code
    # playernumber (0-255) used for IR code
    # colour
    # shots (int)
    # kills (int)
    # ffkills (int)
    # deaths (int)
    # score (int)
    # status (up, down, kicked)
    # state (MQTT state message)

    # TODO methods
    # handle_fire
    # handle_kill
    # handle_death
    # serialise (JSON)
    # deserialise (JSON)
    
    pass