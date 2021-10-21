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
# fx.py
# deals with special effects - laser, RGB, sound
# ----------------------------------------------------------------------

# Handy Colour Constants
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
ORANGE = (255,128,0)
PINK = (255,128,255)
PURPLE = (255,0,255)
CYAN = (0,255,255)
BROWN = (32,10,0) # (64,20,0)

FORWARD = 1
BACKWARD = -1

from time import sleep
from machine import Pin, PWM
import sys, _thread, time
from utils import dbg
from neopixel import NeoPixel
import random
from player import *
import math

DEFAULT_RELOAD_TIME = 5

class FX_Base():
    """
    Base class for all special FX. Subclassed by Laser, RGB and one day Sound.
    It provides methods like fire, reload, hit which can be invoked by events 
    and which deliver the FX in a threaded fashion.
    """
    def fire(self):
        pass
    def firefail(self):
        pass
    def reload(self):
        pass
    def hit(self):
        pass
    def powerup(self):
        pass
    def activate(self):
        pass
    def deactivate(self):
        pass
    def shield(self):
        pass
    def unshield(self):
        pass
    def update(self):
        pass
    def close(self):
        pass

class Laser(FX_Base):
    """
    Provides 'fire-and-forget' threaded methods to do laser special effects.
    """
    def __init__(self, laser_pin, max_brightness, player):
        """
        Initialises the PWM for the laser

        laser_pin: the GPIO pin for the laser
        max_brightness: the max brightness (ie PWM duty cycle, 0-1023)
        player: the current player
        """

        self.laser_pin = laser_pin 
        self.max_brightness = max_brightness
        self.player = player

        self.laser_pwm = PWM(Pin(laser_pin), 500)
        self.off()
        self.fx_busy = False

    def off(self):
        """
        Turn the laser off.
        """
        self.is_on = False
        self.laser_pwm.duty(0)

    def on(self):
        """
        Turn the laser on.
        """
        self.is_on = True
        self.laser_pwm.freq(500)
        self.laser_pwm.duty(self.max_brightness)

    def toggle(self):
        """
        Toggles the laser state.
        """
        if self.is_on:
            self.off()
        else:
            self.on()

    def _blip(self, duration):
        """
        Thread execution method to blip the laser.

        duration: the duration (seconds) for the blip
        """
        self.fx_busy = True
        self.on()
        sleep(duration)
        self.off()
        self.fx_busy = False

    def blip(self, duration):
        """
        Initiates a thread to blip the laser.

        duration: the duration (seconds) for the blip
        """
        _thread.start_new_thread(self._blip, (duration,))
    
    def _strobe(self, frequency, duration):
        """
        Thread execution method to strobe the laser.

        frequency: the frequency (in Hz) for the strobe
        duration: the duration (seconds) to strobe the laser
        """
        self.fx_busy = True
        self.laser_pwm.freq(frequency * 2) # double for cycle of on/off
        self.laser_pwm.duty(self.max_brightness)
        sleep(duration)
        self.off()
        self.fx_busy = False

    def strobe(self, frequency, duration):
        """
        Initiates a thread to strobe the laser.

        frequency: the frequency (in Hz) for the strobe
        duration: the duration (seconds) to strobe the laser
        """
        _thread.start_new_thread(self._strobe, (frequency,duration))

    def close(self):
        """
        Deactivates the laser PWM
        """
        self.off()
        self.laser_pwm.deinit()

    def fire(self):
        """
        Fire effect
        """
        super().fire()
        self.blip(0.25)
    
    def update(self):
        """
        Return the laser to its default state
        """
        # Laser default state is off
        if not self.fx_busy:
            self.off()

class FX(FX_Base):
    """
    Manages a list of FX objects, and invokes the relevant method on them when
    its method is invoked. For example, if the FX object has a Laser and an RGB,
    when you call fx.fire(), it will call laser.fire() and rgb.fire().
    """
    def __init__(self):
        self.fx = []
    
    def trigger_all(self, method_name):
        """
        Invokes the given method on every fx object in the collection

        method: the method to invoke
        """
        for fx in self.fx:
            class_method = getattr(fx, method_name)
            class_method()

    def add(self, fx):
        """
        Adds an fx object to the collection.

        fx: the fx object to add.
        """
        self.fx.append(fx)

    def fire(self):
        self.trigger_all("fire")
    def firefail(self):
        self.trigger_all("firefail")
    def reload(self):
        self.trigger_all("reload")
    def hit(self):
        self.trigger_all("hit")
    def powerup(self):
        self.trigger_all("powerup")
    def activate(self):
        self.trigger_all("activate")
    def deactivate(self):
        self.trigger_all("deactivate")
    def shield(self):
        self.trigger_all("shield")
    def unshield(self):
        self.trigger_all("unshield")
    def update(self):
        self.trigger_all("update")

    

        
class RGB(FX_Base):
    """
    Provides special effects through a collection of WS2812B addressable LEDs.
    """
    def __init__(self, rgb_pin, num_pixels, player):
        """
        Initialises the RGB.

        rgb_pin: the GPIO pin connecting the LEDs.
        num_pixels: the number of connected WS2812B addressable LEDs.
        player: the current player
        """
        self.rgb_pin = rgb_pin 
        self.num_pixels = num_pixels 
        self.reload_time = DEFAULT_RELOAD_TIME
        self.base_colour = (0,0,0)
        self.fx_busy = False # TODO: queue up special effects?
        self.player = player

        self.np = NeoPixel(Pin(rgb_pin), num_pixels)
        self._set_all(self.base_colour)

    ############################################################################
    # Code implementing the special effects
    ############################################################################
    def _set_all(self, colour):
        """
        Sets all pixels to a colour.

        colour: the colour to set the pixels.
        """
        for i in range(0,self.num_pixels):
            self.np[i] = colour
        self.np.write()

    def _set_pixel(self, colour, pixel):
        """
        Sets an individual pixel to a colour.

        colour: the colour to set the pixel.

        pixel: the number of the pixel.
        """
        self.np[pixel] = colour
        self.np.write()

    def _blip_all(self, duration, colour, lastfx):
        """
        Blips all the pixels on one colour, then off.

        duration: the time (seconds) for the pixels to be lit.
        colour: the colour for the pixels.
        lastfx: indicates if this is the 'outer' effect - if true, self.fx_busy is turned Off at the end.
        """
        self.fx_busy = True
        self._set_all(colour)
        sleep(duration)
        self._set_all((0,0,0))

        if lastfx: 
            self.fx_busy = False
            self.update()

    def _strobe_all(self, frequency, duration, colour, lastfx):
        """"
        Strobes all the pixels one colour.

        frequency: strobe rate (Hz)
        duration: the time (seconds) to keep strobing 
        colour: the colour for the pixels
        lastfx: indicates if this is the 'outer' effect - if true, self.fx_busy is turned Off at the end.
        """
        self.fx_busy = True
        halfcycle = (1/frequency)/2

        duration_ms = int(duration * 1000)
        start = time.ticks_ms()
        end = time.ticks_add(start, duration_ms)
        while (time.ticks_ms() < end):
            self._set_all(colour)
            sleep(halfcycle)
            self._set_all((0,0,0))
            sleep(halfcycle)
        
        if lastfx: 
            self.fx_busy = False
            self.update()

    def _calc_colour(self, start, end, progress):
        """
        Calculates the colour for a given 'frame' fading from one colour to another.

        start: the starting colour
        end: the ending colour 
        progress: the progress made so far (float: 0=just starting, 1=finished)
        """
        r_dist = int(((end[0]-start[0]) * progress))
        g_dist = int(((end[1]-start[1]) * progress))
        b_dist = int(((end[2]-start[2]) * progress))
        
        r = start[0] + r_dist
        g = start[1] + g_dist
        b = start[2] + b_dist
        return (r,g,b)

    def _fade_all(self, duration, start_colour, end_colour, frequency, lastfx):
        """
        Fade all pixels from one colour to another.

        duration: the time (seconds) to take for the fade
        start_colour: the starting colour for the pixels
        end_colour: the ending colour for the pixels
        frequency: the rate (Hz) at which to update the pixels.
        lastfx: indicates if this is the 'outer' effect - if true, self.fx_busy is turned Off at the end.
        """
        self.fx_busy = True
        cycle = 1/frequency 

        self._set_all(start_colour)
        duration_ms = int(duration * 1000)
        start = time.ticks_ms()
        end = time.ticks_add(start, duration_ms)
        now = time.ticks_ms()
        while (now < end):
            spent = time.ticks_diff(now, start)
            progress = spent/duration_ms
            
            new_colour = self._calc_colour(start_colour, end_colour, progress)
            
            self._set_all(new_colour)
            time.sleep(cycle)
            now = time.ticks_ms()
        
        self._set_all(end_colour)
        if lastfx: 
            self.fx_busy = False
            self.update()
    
    def _fade_all_log(self, duration, start_colour, end_colour, frequency, lastfx, quickstart):
        """
        Fade all pixels from one colour to another. Logarithmic

        duration: the time (seconds) to take for the fade
        start_colour: the starting colour for the pixels
        end_colour: the ending colour for the pixels
        frequency: the rate (Hz) at which to update the pixels.
        lastfx: indicates if this is the 'outer' effect - if true, self.fx_busy is turned Off at the end.
        quickstart: True - will change quickly at the start, then slowly at the end.
            False - will change slowly at the start, then quickly at the end.
        """
        self.fx_busy = True
        cycle = 1/frequency 

        self._set_all(start_colour)
        duration_ms = int(duration * 1000)
        start = time.ticks_ms()
        end = time.ticks_add(start, duration_ms)
        now = time.ticks_ms()
        while (now < end):
            spent = time.ticks_diff(now, start)
            

            linear = now - start + 1
            if quickstart:
                progress = math.log(linear, duration_ms)# * duration_ms
            else:
                n = duration_ms-linear 
                progress = 1-math.log(duration_ms-linear+1, duration_ms)# * duration_ms
            
            
            new_colour = self._calc_colour(start_colour, end_colour, progress)
            
            self._set_all(new_colour)
            time.sleep(cycle)
            now = time.ticks_ms()
        
        self._set_all(end_colour)
        if lastfx: 
            self.fx_busy = False
            self.update()
    
    

    def _fade_inout_all(self, duration, start_colour, target_colour, frequency, lastfx):
        """
        Fade all pixels from one colour to another and back again.

        duration: the time (seconds) to take for the fade
        start_colour: the starting colour for the pixels
        target_colour: the colour to fade the pixels to
        frequency: the rate (Hz) at which to update the pixels.
        lastfx: indicates if this is the 'outer' effect - if true, self.fx_busy is turned Off at the end.
        """
        self.fx_busy = True
        self._fade_all(duration/2, start_colour, target_colour, frequency, False)
        self._fade_all(duration/2, target_colour, start_colour, frequency, False)
        if lastfx: 
            self.fx_busy = False
            self.update()

    def _fade_inout_all_log(self, duration, start_colour, target_colour, frequency, lastfx):
        """
        Fade all pixels from one colour to another and back again. Logarithmic.

        duration: the time (seconds) to take for the fade
        start_colour: the starting colour for the pixels
        target_colour: the colour to fade the pixels to
        frequency: the rate (Hz) at which to update the pixels.
        lastfx: indicates if this is the 'outer' effect - if true, self.fx_busy is turned Off at the end.
        """
        self.fx_busy = True
        self._fade_all_log(duration/2, start_colour, target_colour, frequency, False, True)
        self._fade_all_log(duration/2, target_colour, start_colour, frequency, False, False)
        if lastfx: 
            self.fx_busy = False
            self.update()
    
    def _pulse_fade(self, duration, start_colour, target_colour, times, frequency, lastfx):
        """
        Fade all pixels from one colour to another and back, a specified number of times.

        duration: the time (seconds) to take for the fade
        start_colour: the starting colour for the pixels.
        target_colour: the colour to fade the pixels to.
        times: the number of cycles to perform.
        frequency: the rate (Hz) at which to update the pixels.
        lastfx: indicates if this is the 'outer' effect - if true, self.fx_busy is turned Off at the end.
        """
        self.fx_busy = True
        for i in range(0,times):
            self._fade_inout_all(duration/times, start_colour, target_colour, frequency, False)
        if lastfx: 
            self.fx_busy = False
            self.update()

    def _crossfade_random(self, duration, start_colour, end_colour, pulses, frequency, lastfx):
        """
        Fades from start to end, through a given number of random colours

        duration: the time (seconds) to take for the effect
        start_colour: the starting colour for the pixels
        end_colour: the ending colour for the pixels
        pulses: the number of colours to fade through
        frequency: the number of times/second the RGB is updated
        lastfx: indicates if this is the 'outer' effect - if true, self.fx_busy is turned Off at the end.
        """
        self.fx_busy = True
        for i in range(0,pulses):
            if i == pulses - 1:
                # last time, go to the end colour
                target = end_colour
            else:
                target = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
            self._fade_all(duration/pulses, start_colour, target, frequency, False)
            start_colour = target
        if lastfx: 
            self.fx_busy = False
            self.update()

    def _wheel(self, pos):
        """
        Input a value 0 to 255 to get a color value.
        Transitions r > g > b > r...
        """
        if pos < 0 or pos > 255:
            return (0, 0, 0)
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        if pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)
    
    def _rainbow_all(self, duration, cycles, frequency, lastfx):
        """
        Cycles through the rainbow (red > green > blue) a specified number of times.

        duration: the time (seconds) to take for the effect
        cycles: the number of times to cycle through the full rainbow.
        frequency: the number of times/second the RGB is updated
        lastfx: indicates if this is the 'outer' effect - if true, self.fx_busy is turned Off at the end.
        """
        self.fx_busy = True

        for i in range(0,cycles):
            cycle = 1/frequency

            start_colour = (255,0,0) 

            self._set_all(start_colour)
            duration_ms = int(duration * 1000/cycles)
            start = time.ticks_ms()
            end = time.ticks_add(start, duration_ms)
            now = time.ticks_ms()
            while (now < end):
                spent = time.ticks_diff(now, start)
                progress = spent/duration_ms
                
                new_colour = self._wheel(int(progress*255))
                
                self._set_all(new_colour)
                time.sleep(cycle)
                now = time.ticks_ms()
            
        self._set_all((0,0,0))
        if lastfx: 
            self.fx_busy = False
            self.update()

    def _rainbow_cycle_all(self, duration, frequency, lastfx):
        """
        Cycles through the rainbow (red > green > blue) a specified number of times.

        duration: the time (seconds) to take for the effect
        cycles: the number of times to cycle through the full rainbow.
        frequency: the number of times/second the RGB is updated
        lastfx: indicates if this is the 'outer' effect - if true, self.fx_busy is turned Off at the end.
        """
        self.fx_busy = True

        ctr = 0

        j = 0

        duration_ms = duration * 1000
        start = time.ticks_ms()
        end = time.ticks_add(start, duration_ms)
        now = start

        wait = 1/frequency
        while (now < end):
            for i in range(self.num_pixels):
                rc_index = (i * 256 // self.num_pixels) + j
                self.np[i] = self._wheel(rc_index & 255)
            self.np.write()
            time.sleep(wait)
            now = time.ticks_ms()
            j += 1
            if j > 255:
                j = 0
            
            
        self._set_all((0,0,0))
        if lastfx: 
            self.fx_busy = False
            self.update()

    def _linear_fill(self, duration, direction, start_colour, end_colour, lastfx):
        """
        Sequentially changes the pixels, like a wipe or progress bar effect.

        duration: the time (seconds) to take for the fill.
        direction: 1 for forward, -1 for backward
        start_colour: the start colour of all the pixels.
        end_colour: the end colour of all the pixels.
        lastfx: indicates if this is the 'outer' effect - if true, self.fx_busy is turned Off at the end.
        """
        # frequency: how many x per second do we update the colour
        self.fx_busy = True
        # TODO: the actual linear fill...
        if lastfx: 
            self.fx_busy = False
            self.update()

    def _linear_pulse(self, duration, direction, background_colour, pixel_colour, lastfx)    :
        """
        Sequentially 'moves' a lit pixel across a fixed background. 

        duration: the time (seconds) to take for the fill.
        direction: 1 for forward, -1 for backward
        background_colour: the background colour of all the pixels.
        pixel_colour: the colour of the lit pixel.
        lastfx: indicates if this is the 'outer' effect - if true, self.fx_busy is turned Off at the end.
        """

        self.fx_busy = True

        print("BG: ")
        print(background_colour)

        print("FG: ")

        time_per_pixel = duration / self.num_pixels 
        # all on 
        if direction == 1:
            start = 0
            step = 1
            stop = self.num_pixels
        else:
            start = self.num_pixels-1
            step = -1
            stop = -1

        self._set_all(background_colour)
        for i in range(start,stop,step):
            self._set_pixel(pixel_colour,i)
            sleep(time_per_pixel)
            self._set_pixel(background_colour,i)
            
        if lastfx: 
            self.fx_busy = False
            self.update()


    ############################################################################
    # Externally-invoked methods
    ############################################################################
    # TODO: should each of these not check self.fx_busy first?
    def fire(self):
        """
        RGB effect for when the gun is fired. A quick linear pulse, background
        is the team colour, the 'lit' pixel is black.
        """
        # a quick _linear_pulse as described
        fx_time = 0.05
        _thread.start_new_thread(self._linear_pulse, (0.05, FORWARD, self.player.team.colour, RED,True))
    
    def bootup(self):
        """
        RGB effect for when the gun boots up. Strobes white for one second
        """
        _thread.start_new_thread(self._strobe_all, (10, 1, WHITE, True))

    def connected(self):
        """
        RGB effect for when the gun is connected to the network. Strobes green 
        for one second
        """
        _thread.start_new_thread(self._strobe_all, (10, 1, GREEN, True))

    def firefail(self):
        """
        RGB effect for when firing fails (eg out of ammo). Strobes red for 
        half a second.
        """
        _thread.start_new_thread(self._strobe_all, (10, 0.5, RED, True))
        
    def reload(self):
        """
        RGB effect for while the gun is reloading. Cycles through the rainbow
        five times.
        """
        start_colour = (0,0,0)
        end_colour = (0, 0, 0)

        _thread.start_new_thread(self._rainbow_cycle_all, (self.reload_time, 1000, True))
        pass
    def hit(self):
        _thread.start_new_thread(self._fade_inout_all_log, (1, self.player.team.colour, BROWN, 50, True))
    def powerup(self):
        # TODO: implement powerup sfx - not needed for prototype?
        pass
    def activate(self):
        _thread.start_new_thread(self._fade_all_log, (1, BLACK, self.player.team.colour, 50, True, False))
        pass
    def deactivate(self):
        _thread.start_new_thread(self._fade_all, (1, self.player.team.colour, BLACK, 50, True))
        pass
    def shield(self):
        # TODO: implement shield SFX - pulsating with white/team colour?
        pass
    def unshield(self):
        # TODO: implement unshield SFX
        pass
    
    def handlestatechange(self, state):
        self.update()

    def update(self):
        """
        Called on state changes to ensure we are showing the right colour.
        Does nothing if fx_busy is True; the effect will call update again
        when it is finished.

        player: the player object (for access to current state)
        """
        print("rgb update")
        if not self.fx_busy:
            print("rgb update: ok")
            if self.player == None:
                print("No player - set to base colour")
                self._set_all(self.base_colour)
            elif self.player.team == None:
                print("No team - set to base colour")
                self._set_all(self.base_colour)
            else:
                colour = self.player.team.colour

                # check for state-specific colour changes
                if self.player.state & UP == 0: # not up, no colour
                    print("Not UP - set to black")
                    colour = BLACK

                if self.player.state & ALIVE == 0: # not alive, no colour
                    colour = (0,0,0)
                
                if self.player.state & KICKED == KICKED: # kicked, no colour
                    colour = (0,0,0)

                if self.player.state & SHIELDED == SHIELDED: # shielded - orange
                    colour = (255,127,0)
                self._set_all(colour)
        else:
            print("rgb update: fx busy")

    def close(self):
        self._set_all(BLACK)