import json

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