#!/usr/bin/python

import os
import sys
import string
from papirus import Papirus
from papirus import PapirusImage
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from time import sleep
import RPi.GPIO as GPIO

# Check EPD_SIZE is defined
EPD_SIZE=0.0
if os.path.exists('/etc/default/epd-fuse'):
    execfile('/etc/default/epd-fuse')
if EPD_SIZE == 0.0:
    print("Please select your screen size by running 'papirus-config'.")
    sys.exit()

# Running as root only needed for older Raspbians without /dev/gpiomem
if not (os.path.exists('/dev/gpiomem') and os.access('/dev/gpiomem', os.R_OK | os.W_OK)):
    user = os.getuid()
    if user != 0:
        print("Please run script as root")
        sys.exit()

# Command line usage
# papirus-buttons

hatdir = '/proc/device-tree/hat'

WHITE = 1
BLACK = 0

SIZE = 27
FLAG = 1

# Assume Papirus Zero
SW1 = 21
SW2 = 16
SW3 = 20 
SW4 = 19
SW5 = 26

# Check for HAT, and if detected redefine SW1 .. SW5
if (os.path.exists(hatdir + '/product')) and (os.path.exists(hatdir + '/vendor')) :
   f = open(hatdir + '/product')
   prod = f.read()
   f.close()
   f = open(hatdir + '/vendor')
   vend = f.read()
   f.close
   if (string.find(prod, 'PaPiRus ePaper HAT') == 0) and (string.find(vend, 'Pi Supply') == 0) :
       # Papirus HAT detected
       SW1 = 16
       SW2 = 26
       SW3 = 20
       SW4 = 21
       SW5 = -1

def main():
    global SIZE
    global FLAG
    
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(SW1, GPIO.IN)
    GPIO.setup(SW2, GPIO.IN)
    GPIO.setup(SW3, GPIO.IN)
    GPIO.setup(SW4, GPIO.IN)
    if SW5 != -1:
        GPIO.setup(SW5, GPIO.IN)

    papirus = Papirus()
    screen = PapirusImage()

    # Use smaller font for smaller dislays
    if papirus.height <= 96:
        SIZE = 18

    papirus.clear()

    # Initialize Screen
    screen.write('./images/light1.bmp')
    while True:
        # Exit when SW1 and SW2 are pressed simultaneously
        if (GPIO.input(SW1) == False) and (GPIO.input(SW2) == False) :
            write_text(papirus, "Exiting ...", SIZE)
            sleep(0.2)
            papirus.clear()
            sys.exit()

        if GPIO.input(SW1) == False:
            if FLAG == 4:
                FLAG = 1
            else:
                FLAG += 1
            write_text(papirus, "placeholder", SIZE, FLAG)

        if GPIO.input(SW2) == False:
            if FLAG == 1:
                FLAG = 4
            else:
                FLAG -= 1
            write_text(papirus, "placeholder", SIZE, FLAG)

        #if GPIO.input(SW3) == False:
            #write_text(papirus, "Three", SIZE)

        #if GPIO.input(SW4) == False:
            #write_text(papirus, "Four", SIZE)

        #if (SW5 != -1) and (GPIO.input(SW5) == False):
            #write_text(papirus, "Five", SIZE)
 
        sleep(0.1)

def write_text(papirus, text, size, flag):

    screen = PapirusImage()
    print(flag)
    
    if flag == 1:
        screen.write('./images/light1.bmp')

    
    if flag == 2:
        screen.write('./images/light2.bmp')

    if flag == 3:
        screen.write('./images/tv.bmp')

    if flag == 4:
        screen.write('./images/fan.bmp')
        
if __name__ == '__main__':
    main()