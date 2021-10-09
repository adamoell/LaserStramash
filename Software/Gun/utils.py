# Laser Stramash: the openest, coolest laser tag system
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
# utils.py
# assorted utilities
# ----------------------------------------------------------------------

import random
import ujson
import sys, machine

SOFT = 0
HARD = 1

def dbg(msg):
    """
    Prints a message - comment out for production use.
    """
    print(msg)

class Config():
    def __init__(self, config_file="config.json"):
        self.config = None
        with open(config_file) as f:
            self.config = ujson.load(f)

    def get(self, key):
        """
        Retrieve a config value.
        
        key: a string in the format "section:key"
        """
        try:
            items = key.split(":")
            return self.config[items[0]][items[1]]  
        except:
            raise KeyError
    
    def get_int(self, key):
        return int(self.get(key))


def unique_id(length=8):
    """
    Generates a random unique identifier.
    """
    #alphabet = string.ascii_letters + digits
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz01234567890"
    return ''.join(random.choices(alphabet, k=length))

def inttohexstring(val, width=4):
    """
    Turn an int into a 4-byte hex string
    """
    s = hex(val)[2:]
    return '{:0>{w}}'.format(s, w=width)

def reset(reason, type):
    if type == "SOFT":
        dbg("Soft Reset: "+reason)
        sys.exit() # soft reset
    else:
        dbg("Hard Reset: "+reason)
        machine.reset() # hard reset