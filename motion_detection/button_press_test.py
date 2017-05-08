
import logging
import sys
import time
import RPi.GPIO as GPIO

from pylab import *
from Adafruit_BNO055 import BNO055
from mdAlgorithm import getShape

# Enable verbose debug logging if -v is passed as a parameter.
if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)

bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)

# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

# Print system status and self test result.
status, self_test, error = bno.get_system_status()
print('System status: {0}'.format(status))
print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
# Print out an error if system status is in error mode.
if status == 0x01:
    print('System error: {0}'.format(error))
    print('See datasheet section 4.3.59 for the meaning.')                                                                                                                         


# Print BNO055 software revision and other diagnostic data.
sw, bl, accel, mag, gyro = bno.get_revision()
print('Software version:   {0}'.format(sw))
print('Bootloader version: {0}'.format(bl))
print('Accelerometer ID:   0x{0:02X}'.format(accel))
print('Magnetometer ID:    0x{0:02X}'.format(mag))
print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))

print('Reading BNO055 data, press Ctrl-C to quit...')


# GPIO Setup for button
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#variable for controlling debug print statemnts
debug=0
#debug=1

# Lists for storing readings between button pushes
heading = []
roll = []
pitch = []



#main loop 

while True:
    input_state = GPIO.input(24)
    if input_state == False:
        # print('Button Pressed')         
        # Read the Euler angles for heading, roll, pitch (all in degrees).
        heading_temp, pitch_temp, roll_temp = bno.read_euler()
        # store orientation angles into list arrays
        heading.append(heading_temp)
        roll.append(roll_temp)
        pitch.append(pitch_temp)
        # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
        sys, gyro, accel, mag = bno.get_calibration_status()
        time.sleep(.01)

    elif len(heading) != 0:
        # Print everything out.

	print getShape(heading,pitch)
	
        # Reset heading list
        heading = []
        pitch = []

