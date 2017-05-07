
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

#variable for controlling debug print statemnts
debug = 0
#debug=1

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

	if debug==1:
	    print "heading list: "


	rounded_heading = []
	rounded_pitch =[]

	rounded_heading = round_angles(heading)
	rounded_pitch = round_angles(pitch)

	rounded_heading = np.array(rounded_heading)
	rounded_pitch = np.array(rounded_pitch)

	# Center heading
	centered_heading = rounded_heading[:]-rounded_heading[1]
	
	if debug==1:
	    print "Centered heading data: "
	    print centered_heading
	    print "Pitch data: "
	    print rounded_pitch

	# Convert heading data to project position data
	position_array_length = len(centered_heading[:])

	if debug==1:
	    print "Array Length: "
	    print position_array_length

	pitch_array_length = len(rounded_pitch[:])

	if debug==1:
	    print "pitch array length: "
	    print pitch_array_length 

	heading_array_length = len(rounded_heading[:])

	if debug==1:
 	    print "heading array length: "
	    print heading_array_length

	#Convert heading and pitch angles into cartesion coordinates
        #y_length was arbitrarily set to 10
	y_length = 10
	x_position = y_length * np.tan(np.deg2rad(centered_heading[:]))
	y_position = y_length * np.tan(np.deg2rad(rounded_pitch[:]))

	if debug==1:
	    print "x_position array: "
	    print x_position

	    print "y_position array: "
	    print y_position

	data_points = np.vstack((x_position,y_position))

	if debug==1:	
	    print "data points: "
	    print data_points

	#generate vectors from data_points
	vectors = np.zeros((position_array_length,3))

	#create vectors connecting each points
	for k in range(0,position_array_length-2):
	    vectors[k,0] = data_points[0,k+1] - data_points[0,k];
            vectors[k,1] = data_points[1,k+1] - data_points[1,k];

	#creates final vector between starting and ending points
	vectors[position_array_length-1,0] =  data_points[0,position_array_length-1] - data_points[0,0];
    	vectors[position_array_length-1,1] =  data_points[1,position_array_length-1] - data_points[1,0];

	if debug==1: 
	    print "Vectors Array: "
	    print vectors

	#remove duplicate vectors from array
	vectors = vectors[~(vectors==0).all(1)]

	if debug==1:
	    print "Vectors with duplicates removed: "
	    print vectors

	#generate array of vector angles by reference vector array to a zero degree reference vector
	ref_vector = [1,0,0]
	cross_variable = np.cross(ref_vector,vectors)
	vector_array_length = len(vectors)

	
	vector_angles = []	

	for k in range(0,vector_array_length-1): 
	    dot_product = np.dot(ref_vector,vectors[k])
	    np.arctan2(cross_variable[:,2],np.dot(ref_vector,vectors[k]))
            vector_angles.append( np.arctan2(cross_variable[k,2],np.dot(ref_vector,vectors[k]))*180/pi)

	if debug==1:
	    print "Vector Angles List: "
	    print np.around(vector_angles)


	#replace negative angles to form unit circle values from 0 to 360 degrees
	for k in range(0,vector_array_length-1):
	    if vector_angles[k] <= 0:
		vector_angles[k] = 360 + vector_angles[k]

	if debug==1:
            print "Vector Angles List: "
            print np.around(vector_angles)

	#bin vector angles for frequency analysis
	edges = np.linspace(0,360, 73)  #0 5 10 ...360
	frequency_hist = np.histogram(vector_angles,edges)

	if debug==1:
	    print "Freqency Bins: "
	    print frequency_hist[0]
	
	frequency_hist = np.array(frequency_hist[0])

	#generate shape charactersistics that can be used to identify drawn shape
	dominant_angle_number = len(frequency_hist[np.where(frequency_hist > 4)])
	dominant_angle_index = np.argmax(frequency_hist)
	dominant_angle_value = 5*dominant_angle_index

	print "Dominant Angle: "
	print dominant_angle_value	

	#Use frequency analysis to determine shape drawn
	choices = {1: 'line', 3: 'triangle', 4: 'square', 0: 'circle' }
	result = choices.get(dominant_angle_number, 'Sorry no ID made! Try again...')

	print "Shape Matched: "
	print result

	# Reset heading list
	heading = []
	pitch = []
	
