from roku import Roku
from time import sleep
from phue import Bridge
import logging
import random
logging.basicConfig()

b = Bridge('192.168.0.117')

b.connect()

b.get_api()

lights = b.get_light_objects()

def roku_command(remote_command):
    delay = 1

    #connect to roku
    #enter your rokus ip address to test
    roku = Roku('192.168.0.110')

    #remote command is place holder for list of commands from remote to dashboard
    #remote_command=['triangle']

    #if circle shape is registered on remote than launch the most recent episode of a users favorite show.
    #In this case Silicon Valley.
    for i in remote_command:
        if i == 'circle':

            for light in lights:
                light.brightness = 254
                light.xy = [.1,.1]

            hbo = roku["HBO GO"]
            hbo.launch()

            sleep(6*delay)

            roku.down()
            sleep(delay)

            roku.right()
            sleep(delay)

            roku.right()
            sleep(delay)

            roku.select()
            sleep(3*delay)

	    roku.select()
	    sleep(2*delay)

	    roku.select()
	    sleep(delay)	    
#            roku.up()
#            sleep(delay)

#            roku.left()
#            sleep(delay)

#            roku.down()
#            sleep(delay)

#            roku.left()
#            sleep(delay)

#            roku.select()
#            sleep(2*delay)

#            roku.right()
#            sleep(delay)

#            roku.select()
#            sleep(2*delay)

#            roku.select()
#            sleep(2*delay)

            for light in lights:
                light.brightness = 100

        if i == "left_swipe":
            #move cursor left
            roku.left()

	if i == "up_swipe":
	    roku.up()

	if i == "down_swipe":
	    roku.down()

        if i == "right_swipe":
            #move curser right
            roku.right()

        if i == "triangle":
	    print "test"
	    b.set_light([2,3], 'on', True)

	    # Prints if light 1 is on or not
	    b.get_light(2, 'on')

	    # Set brightness of lamp 1 to max
	    b.set_light(2, 'bri', 254)

	    # Set brightness of lamp 2 to 50%
	    b.set_light(3, 'bri', 254)

	    for light in lights:
		light.brightness = 254
		light.xy = [.9,.7]	
            #enter search commands
            roku.search()

        if i == "square":
            roku.info()

	if i == 'quad_diagonal_1':
	    b.set_light(1, 'on', False)

    return True

#variable = "circle"
#list=[]
#list.append(variable)
#roku_command(list)
