# Laser Stramash 
VERSION = "0.0.1"

# Copyright (C) 2021 by Adam Oellermann

from sys import platform
import time
import gc
from machine import TouchPad, Pin, freq
from ir_rx.print_error import print_error  # Optional print of error codes
from ir_rx.nec import NEC_8, NEC_16
import ujson
from networking import *
from buttons import *
from ir_tx.nec import NEC
import neopixel

ir_on = False
laser_pin = None
laser_brightness = 0
laser_pwm = None

def dbg(msg):
    print(msg)
    mqtt_send("dbg", msg)

# open up the config
config = None
with open("ls.json") as f:
    config = ujson.load(f)

def padstring(s, width):
    return '{:0>{w}}'.format(s, w=width)

# Send an NEC pulse
def send_ir(addr, data):
    global ir_sender
    ir_sender.transmit(addr, data)  # address == 1, data == 2

# handle received IR code
def handle_ir(data, addr, ctrl): 
    global id   
    if data > 0: # ignore repeat codes
        data_hex = padstring(hex(data)[2:], 4)
        addr_hex = padstring(hex(addr)[2:], 4)
        hitby = addr_hex + ":" +data_hex
        print(id + " hit by "+hitby)
        mqtt_send("hit", hitby+">"+id)

def strobe_laser(duration):
    global laser_pwm, laser_brightness

    laser_pwm.freq(20)
    laser_pwm.duty(laser_brightness)
    sleep(duration)
    laser_pwm.duty(0)

def pulse_laser(duration):
    global laser_pwm, laser_brightness

    laser_pwm.freq(500)
    laser_pwm.duty(laser_brightness)
    sleep(duration)
    laser_pwm.duty(0)

# handle pressed buttons
def handle_fire(arg=None):
    dbg("Fire pressed")
    send_ir(0x7e,0x2a)
    pulse_laser(0.1)


def handle_reload(arg=None):
    dbg("Reload pressed")
    
    strobe_laser(0.5)

def demo(np):
    n = np.n

    # cycle
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 0)
        np[i % n] = (255, 255, 255)
        np.write()
        time.sleep_ms(25)

    # bounce
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 128)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0)
        np.write()
        time.sleep_ms(60)

    # fade in/out
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (val, 0, 0)
        np.write()

    # clear
    for i in range(n):
        np[i] = (0, 0, 0)
    np.write()
ls_version = config['Game']['version']
    
hdr = "Laser Stramash "+ls_version
dbg(hdr)
dbg("-"*len(hdr))

# clock faster for IR
#machine.freq(160000000)
machine.freq(240000000)
dbg('ESP32 running at ' + str(machine.freq()))
# who am I?

def wheel(pos):
  #Input a value 0 to 255 to get a color value.
  #The colours are a transition r - g - b - back to r.
  if pos < 0 or pos > 255:
    return (0, 0, 0)
  if pos < 85:
    return (255 - pos * 3, pos * 3, 0)
  if pos < 170:
    pos -= 85
    return (0, 255 - pos * 3, pos * 3)
  pos -= 170
  return (pos * 3, 0, 255 - pos * 3)

def setcolour(rgb, colour):
    rgb[0] = colour
    rgb.write()

# setup LEDs
dbg('Setting up LEDs...')
print("Laser")
laser_pin = Pin(int(config['Hardware']['laser_pin']))
print(laser_pin)
laser_pwm = machine.PWM(laser_pin, 500)
laser_brightness = int(config['Hardware']['laser_brightness']) # 0=off, 1023=max
laser_pwm.duty(0)

print("RGB")
rgb_pin = Pin(int(config['Hardware']['rgb_pin']))
print(rgb_pin)
rgb = neopixel.NeoPixel(rgb_pin, 1)

setcolour(rgb, (128,128,128))

touch_pin = Pin(int(config['Hardware']['reload_pin']))
tp = TouchPad(touch_pin)



def pew(rgb):
    for i in range(0,3):
        setcolour(rgb, (255,0,0))
        sleep(0.1)
        setcolour(rgb, (0,255,0))
        sleep(0.1)
        setcolour(rgb, (0,0,255))
        sleep(0.1)
        setcolour(rgb, (128,128,128))

try:
    while True:
        val = tp.read()
        print(val)
        sleep(0.2)
        if val < 500:
            pew(rgb)
except KeyboardInterrupt:
    setcolour(rgb, (0,0,0))

# try:
#     while True:
#         for i in range(0,256):
#             rgb[0] = wheel(i)
#             rgb.write()
#             sleep(0.025)
        
#         for j in range(0,5):
#             for i in range(0,256):
#                 rgb[0] = (i, i, i)
#                 rgb.write()
#                 sleep(0.002)
#             for i in range(255,-1,-1):
#                 rgb[0] = (i, i, i)
#                 rgb.write()
#                 sleep(0.002)
# except KeyboardInterrupt:
#     rgb[0] = (0,0,0)
#     rgb.write()

