from pylab import *

def getShape(heading,pitch):
	
    rounded_heading = []
    rounded_pitch =[]

    rounded_heading = round_angles(heading)
    rounded_pitch = round_angles(pitch)

    rounded_heading = np.array(rounded_heading)
    rounded_pitch = np.array(rounded_pitch)

    # Center heading
    centered_heading = rounded_heading[:]-rounded_heading[1]

    # Convert heading data to project position data
    position_array_length = len(centered_heading[:])

    pitch_array_length = len(rounded_pitch[:])

    heading_array_length = len(rounded_heading[:])

    #Convert heading and pitch angles into cartesion coordinates
    #y_length was arbitrarily set to 10
    y_length = 10
    x_position = y_length * np.tan(np.deg2rad(centered_heading[:]))
    y_position = y_length * np.tan(np.deg2rad(rounded_pitch[:]))

    data_points = np.vstack((x_position,y_position))

    #generate vectors from data_points
    vectors = np.zeros((position_array_length,3))

    #create vectors connecting each points
    for k in range(0,position_array_length-2):
        vectors[k,0] = data_points[0,k+1] - data_points[0,k];
        vectors[k,1] = data_points[1,k+1] - data_points[1,k];

    #creates final vector between starting and ending points
    vectors[position_array_length-1,0] =  data_points[0,position_array_length-1] - data_points[0,0];
    vectors[position_array_length-1,1] =  data_points[1,position_array_length-1] - data_points[1,0];

    #remove duplicate vectors from array
    vectors = vectors[~(vectors==0).all(1)]

    #generate array of vector angles by referencing vector array to a zero degree vector
    ref_vector = [1,0,0]
    cross_variable = np.cross(ref_vector,vectors)
    vector_array_length = len(vectors)

    vector_angles = []

    for k in range(0,vector_array_length-1):
        dot_product = np.dot(ref_vector,vectors[k])
        np.arctan2(cross_variable[:,2],np.dot(ref_vector,vectors[k]))
        vector_angles.append( np.arctan2(cross_variable[k,2],np.dot(ref_vector,vectors[k]))*180/pi)

    #replace negative angles to form unit circle values from 0 to 360 degrees
    for k in range(0,vector_array_length-1):
        if vector_angles[k] <= 0:
            vector_angles[k] = 360 + vector_angles[k]

    #bin vector angles for frequency analysis
    edges = np.linspace(0,360, 73)  #0 5 10 ...360
    frequency_hist = np.histogram(vector_angles,edges)

    frequency_hist = np.array(frequency_hist[0])

    #generate shape charactersistics that can be used to identify drawn shape
    dominant_angle_number = len(frequency_hist[np.where(frequency_hist > 4)])
    dominant_angle_index = np.argmax(frequency_hist)
    dominant_angle_value = 5*dominant_angle_index

    result = []
    result.append(dominant_angle_value)

    #Use frequency analysis to determine shape drawn
    choices = {1: 'line', 3: 'triangle', 4: 'square', 0: 'circle' }
    result.append(choices.get(dominant_angle_number, 'Sorry no ID made! Try again...'))
    shape = choices.get(dominant_angle_number, 'Sorry no ID made! Try again...')

    print "Dominant Angle: "
    print dominant_angle_value
    print "Shape: "
    print shape

    return (dominant_angle_value, shape)
	 
def round_angles(array):
    rounded_angle = []

    for numbers in array:
        rounded_angle.append( int(round(numbers)))
    return rounded_angle

