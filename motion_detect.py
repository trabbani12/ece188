import logging
import sys
import time
import RPi.GPIO as GPIO 

from pylab import *
from Adafruit_BNO055 import BNO055

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

# Lists for storing readings between button pushes
heading = []
roll = []
pitch = []

#functions 
def round_angles(array):
    rounded_angle = []

    for numbers in array:
        rounded_angle.append( int(round(numbers)))
    return rounded_angle

def angle2xy(y_length, heading, pitch):

    x_position = y_length * np.tan(heading[:])
    y_position = y_length * np.tan(pitch[:])

    data_points = np.vstack((x_position,y_position))
    return data_points

def shape_id(heading):
    rounded_heading = []
    print "rounded heading list: "
    print heading
    return
#main loop 


#main loop 

while True:
    input_state = GPIO.input(24)
    if input_state == False:
	print('Button Pressed')	  
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
	print "heading list: "


	rounded_heading = []
	rounded_pitch =[]

	rounded_heading = round_angles(heading)
	rounded_pitch = round_angles(pitch)

	rounded_heading = np.array(rounded_heading)
	rounded_pitch = np.array(rounded_pitch)

	# Center heading
	centered_heading = rounded_heading[:]-rounded_heading[1]
	print "Centered heading data: "
	print centered_heading

	print "Pitch data: "
	print rounded_pitch

	# Convert heading data to project position data
	position_array_length = len(centered_heading[:])
	print "Array Length: "
	print position_array_length

	pitch_array_length = len(rounded_pitch[:])
	print "pitch array length: "
	print pitch_array_length 

	heading_array_length = len(rounded_heading[:])
	print "heading array length: "
	print heading_array_length

	#data_points = angle2xy(10, centered_heading[:], rounded_pitch[:])
	y_length = 10
	x_position = y_length * np.tan(np.deg2rad(centered_heading[:]))
	y_position = y_length * np.tan(np.deg2rad(rounded_pitch[:]))

	print "x_position array: "
	print x_position

	print "y_position array: "
	print y_position

	data_points = np.vstack((x_position,y_position))
	
	print "data points: "
	print data_points

	#generate vectors from data_points
	vectors = np.zeros((position_array_length,2))

	#create vectors connecting each points
	for k in range(0,position_array_length-2):
	    vectors[k,0] = data_points[0,k+1] - data_points[0,k];
            vectors[k,1] = data_points[1,k+1] - data_points[1,k];

	#creates final vector between starting and ending points  **MAY NEED TO BE REMOVED***
	vectors[position_array_length-1,0] =  data_points[0,position_array_length-1] - data_points[0,0];
    	vectors[position_array_length-1,1] =  data_points[1,position_array_length-1] - data_points[1,0];

	print "Vectors Array: "
	print vectors
	
	vectors = vectors[~(vectors==0).all(1)]
	print "Vectors with duplicates removed: "
	print vectors

	shape_id(rounded_heading)
	# Reset heading list
	heading = []
	pitch = []
	
