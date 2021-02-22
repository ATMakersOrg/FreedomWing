# CircuitPython AnalogIn Demo
import time
import board
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
import array
import adafruit_ds3502

import neopixel
led = neopixel.NeoPixel(board.NEOPIXEL, 1)
led.brightness = .3
led[0] = (0,1,200)

def range_map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)


i2c = board.I2C()
vPot = adafruit_ds3502.DS3502(i2c,0x2a)
hPot = adafruit_ds3502.DS3502(i2c,0x2b)

ref = AnalogIn(board.A2)
hor = AnalogIn(board.A3)
vert = AnalogIn(board.A4)

hPot.wiper = vPot.wiper = 0
time.sleep(.1)
rVal = ref.value
hVal = hor.value
vVal = vert.value
#print((rVal,hVal,vVal,hVal-rVal,vVal-rVal) )
hMin = hVal
vMin = vVal
rMin = rVal

hPot.wiper = vPot.wiper = 127
time.sleep(.1)
rVal = ref.value
hVal = hor.value
vVal = vert.value
#print((rVal,hVal,vVal,hVal-rVal,vVal-rVal) )
hMax = hVal
vMax = vVal
rMax = rVal

vTarget =  vMin + ((vMax - vMin)) / 2.0
vCloseN = -1
vCloseVal = None
hTarget = hMin + ((hMax - hMin)) / 2.0
hCloseN = -1
hCloseVal = None
for n in range(0, 128):
    hPot.wiper = n
    vPot.wiper = n
    time.sleep(.025)
    hVal = hor.value
    vVal = vert.value

    if (vCloseN == -1 or (abs(vVal - vTarget) < abs(vCloseVal - vTarget))):
        vCloseN = n
        vCloseVal = vVal
    if (hCloseN == -1 or (abs(hVal - hTarget) < abs(hCloseVal - hTarget))):
        hCloseN = n
        hCloseVal = hVal
    print((hCloseN, hCloseVal, (hMax - hMin), vCloseN, vCloseVal, (vMax - vMin)) )
    #print(n, vVal, vCloseVal, vTarget, hVal, hCloseVal, hTarget)

#print((hCloseN, hCloseVal, (hMax - hMin), vCloseN, vCloseVal, (vMax - vMin)) )

if (abs(hCloseN - 63) < 6 and abs(vCloseN - 63) < 6):
    led[0] = (0,200,000)
else:
    led[0] = (0,0,0)
while True:
    time.sleep(10)
