#***************************************************************************
#* File Name: Xbox/python/code.py
#* Title: FreedomWing Code
#* Developed by: ATMakers
#* Version Number: 1.1 (23/9/2022)
#* Github Link: https://github.com/ATMakersOrg/FreedomWing
#***************************************************************************/

# Import modules
import time
import board
import array
import usb_hid
from analogio import AnalogIn
from hid_xac_gamepad import Gamepad
from settings import *


time.sleep(1.0)
# Create an object instance of Gamepad class
gp = Gamepad(usb_hid.devices)

# RollingAverage Class
class RollingAverage:
    def __init__(self, size):
        self.size=size
        self.buffer = array.array('d')
        for i in range(size):
            self.buffer.append(0.0)
        self.pos = 0
    def addValue(self,val):
        self.buffer[self.pos] = val
        self.pos = (self.pos + 1) % self.size
    def average(self):
        return (sum(self.buffer) / self.size)

# Define Alanlog input pins
if (not legacyPinout):
    base = AnalogIn(board.A1)
    if (not swapAxes):
        hor = AnalogIn(board.A2)
        vert = AnalogIn(board.A3)
    else:
        hor = AnalogIn(board.A3)
        vert = AnalogIn(board.A2)
else:
    base = AnalogIn(board.A2)
    if (not swapAxes):
        hor = AnalogIn(board.A3)
        vert = AnalogIn(board.A4)
    else:
        hor = AnalogIn(board.A4)
        vert = AnalogIn(board.A3)
        
# Define axis invertion state
if (not invertHor):
    horDirection=1
else:
    horDirection=-1

if (not invertVert):
    vertDirection=1
else:
    vertDirection=-1


# Create arrays to calculate rolling average values
avgCount = smoothingFactor
baseAvg = RollingAverage(avgCount)
horAvg = RollingAverage(avgCount)
vertAvg = RollingAverage(avgCount)

# Input to output mapping function
def range_map(value, in_min, in_max, out_min, out_max):
    return int(max(out_min,min(out_max,(value - in_min) * (out_max - out_min) // (in_max - in_min) + out_min)))

# Get Voltage function returns the voltage reading of the analog pin via ADC
def get_voltage(pin):
    return (pin.value)
    
# Initialize base reading
baseVal = 0

# Set the horizontal and vertical base value to avarage of 10 readings
for i in range(0,10,1):
   baseVal += (get_voltage(base))/10.0
   time.sleep(.1)

# Set the high end and low end of voltage changes 
# baseVal : ( 6V x (47KOhm / 147 KOhm ) ) = ~1.9V 
# lowVal  : ( -1.2V x (47KOhm / 147 KOhm ) ) = ~-0.38V or -1.9V/6
# highVal : ( 1.2V x (47KOhm / 147 KOhm ) ) = ~0.38V or 1.9V/6
lowVal = -(baseVal / 6)
highVal = (baseVal / 6)

# Initialize variables and set constants
center = 128
last_game_x = center
last_game_y = center

game_thresh=1
middleLimit = 10

# Reset gamepad HID
gp.reset_all()

while True:
    # Update input reading and calculate the changes from base
#    baseVal = get_voltage(base)
    horVal = get_voltage(hor) - baseVal
    vertVal = get_voltage(vert) - baseVal
    
    # Debug inputs
    if (debugEnabled == True):
        print("Input: ",(baseVal, horVal, vertVal,))
    
    # Add new horizontal and vertical values to RollingAverage arrays
    horAvg.addValue(horVal)
    vertAvg.addValue(vertVal)

    # Map average input readings to output values based on low end and high end values
    game_x = range_map(horDirection * horAvg.average(), lowVal, highVal, 0, 255)
    game_y = range_map(vertDirection * vertAvg.average(), lowVal, highVal, 0, 255)

    # Deadband logic
    if (abs(game_x - center) < middleLimit):
        game_x = center
    if (abs(game_y - center) < middleLimit):
        game_y = center

    # Output x and y values to host devices 
    if (abs(last_game_x - game_x) > game_thresh):
        last_game_x = game_x
        gp.move_joysticks(x=game_x)
    if (abs(last_game_y - game_y) > game_thresh):
        last_game_y = game_y
        gp.move_joysticks(y=game_y)
    # Debug average inputs and mapped outputs
    if (debugEnabled == True):
        print("Average: ",(horAvg.average(),vertAvg.average(),))
        print("Output: ",(game_x, game_y,))
    time.sleep(0.025)