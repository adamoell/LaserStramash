# MIT License
# Copyright 2017 Christopher Arndt
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#-------------------------------------------------------------------------------
# Obtained here: https://gist.github.com/SpotlightKid/0a0aac56606286a80f860b116423c94f
# inspired by: https://forum.micropython.org/viewtopic.php?t=1938#p10931
# Lightly edited by Adam Oellermann for Laser Stramash
#-------------------------------------------------------------------------------
import micropython

from machine import Timer
timer_init = lambda t, p, cb: t.init(period=p, callback=cb)

# uncomment when debugging callback problems
#micropython.alloc_emergency_exception_buf(100)


class DebouncedSwitch:
    def __init__(self, sw, cb, arg=None, delay=50, tid=4):
        self.sw = sw
        # Create references to bound methods beforehand
        # http://docs.micropython.org/en/latest/pyboard/library/micropython.html#micropython.schedule
        self._sw_cb = self.sw_cb
        self._tim_cb = self.tim_cb
        self._set_cb = getattr(self.sw, 'callback', None) or self.sw.irq
        self.delay = delay
        self.tim = Timer(tid)
        self.callback(cb, arg)

    def sw_cb(self, pin=None):
        self._set_cb(None)
        timer_init(self.tim, self.delay, self._tim_cb)

    def tim_cb(self, tim):
        tim.deinit()
        #if not self.sw(): # fires on 'released' AO changed to fire on pressed
        if not self.sw(): # fires on 'pressed' 
            micropython.schedule(self.cb, self.arg)
        self._set_cb(self._sw_cb if self.cb else None)

    def callback(self, cb, arg=None):
        self.tim.deinit()
        self.cb = cb
        self.arg = arg
        self._set_cb(self._sw_cb if cb else None)
