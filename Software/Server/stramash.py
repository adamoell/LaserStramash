import json

class Game:
    # TODO properties
    # id - short GUID - 
    #   generate using something like urlsafe_b64encode(os.urandom(6)) (import base64, os)
    #   or better still
    #       alphabet = string.ascii_letters + string.digits
    #       >>> ''.join(random.choices(alphabet, k=8))
    # name
    # start_time
    # players
    # teams
    # status: 0=Unstarted, 1=Active, 2=Finished
    # state (MQTT state message)

    # TODO methods
    # serialise (JSON)
    # deserialise (JSON)
    # save
    # load
    # addplayer
    # deleteplayer
    # addteam
    # deleteteam

    pass

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

class Team:
    # TODO properties
    # name
    # id
    # colour
    # players
    # state (MQTT state message)

    # TODO methods
    # addplayer
    # deleteplayer
    # serialise (JSON)
    # deserialise (JSON)

    pass

class ColourOutOfRange(Exception):
    pass

class Colour:
    def __init__(self, name, red, green, blue):
        self.name = name
        self.red = red 
        self.blue = blue 
        self.green = green 

    # name
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name

    # red
    @property
    def red(self):
        return self._red
    @red.setter
    def red(self, red):
        if (red > 255) or (red < 0):
            raise ColourOutOfRange
        self._red = red

    # green
    @property
    def green(self):
        return self._green
    @green.setter
    def green(self, green):
        if (green > 255) or (green < 0):
            raise ColourOutOfRange
        self._green = green

    # blue
    @property
    def blue(self):
        return self._blue
    @blue.setter
    def blue(self, blue):
        if (blue > 255) or (blue < 0):
            raise ColourOutOfRange
        self._blue = blue

    # TODO methods
    def serialise(self):
        return('["'+self.name+'",'+str(self.red)+','+str(self.green)+','+str(self.blue)+']')
    
    @staticmethod
    def deserialise(serialised_colour):
        data = json.loads(serialised_colour)
        colour = Colour(data[0], data[1], data[2], data[3])
        return colour

    # serialise (JSON)
    # deserialise (JSON)

if __name__ == '__main__':
    green_serialised = '["Green",0,255,0]'
    green = Colour.deserialise(green_serialised)
    print(green.serialise())