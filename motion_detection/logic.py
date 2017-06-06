from roku import Roku
from time import sleep




def roku_command(remote_command):
    delay = 1

    #connect to roku
    #enter your rokus ip address to test
    roku = Roku('192.168.0.110')

    #remote command is place holder for list of commands from remote to dashboard
    #remote_command=[]

    #if circle shape is registered on remote than launch the most recent episode of a users favorite show.
    #In this case Silicon Valley.
    for i in remote_command:
        if i == 'circle':

            hbo = roku["HBO GO"]
            hbo.launch()

            sleep(6*delay)

            roku.down()
            sleep(delay)

            roku.down()
            sleep(delay)

            roku.right()
            sleep(delay)

            roku.select()
            sleep(3*delay)

            roku.up()
            sleep(delay)

            roku.left()
            sleep(delay)

            roku.down()
            sleep(delay)

            roku.left()
            sleep(delay)

            roku.select()
            sleep(2*delay)

            roku.right()
            sleep(delay)

            roku.select()
            sleep(2*delay)

            roku.select()
            sleep(2*delay)

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
            #enter search commands
            roku.search()

        if i == "square":
            roku.info()

    return True

#variable = "right_swipe""
#list=[]
#list.append(variable)
#roku_command(list)
