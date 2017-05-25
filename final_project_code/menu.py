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
import ouimeaux
from ouimeaux.environment import Environment
from phue import Bridge
from pymongo import MongoClient

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

        # Up Arrow
        if GPIO.input(SW1) == False:
            if FLAG == 4:
                FLAG = 1
            else:
                FLAG += 1
            write_text(papirus, "placeholder", SIZE, FLAG)

        # Down Arrow
        if GPIO.input(SW2) == False:
            if FLAG == 1:
                FLAG = 4
            else:
                FLAG -= 1
            write_text(papirus, "placeholder", SIZE, FLAG)

        # Function 3
        if GPIO.input(SW3) == False:
            function_three(FLAG)

        # Function 2
        if GPIO.input(SW4) == False:
            function_two(FLAG)

        # Function 1
        if (SW5 != -1) and (GPIO.input(SW5) == False):
            function_one(FLAG)
 
        sleep(0.05)

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

def function_one(flag):
    # Initialization
    env = Environment()
    env.start()
    env.discover(3)
    b = Bridge('192.168.0.100')
    b.connect()
    lights = b.lights
    groups = b.groups
    client = MongoClient('mongodb://tmega:ucsdece188!@tmega-shard-00-00-kcfpq.mongodb.net:27017,tmega-shard-00-01-kcfpq.mongodb.net:27017,tmega-shard-00-02-kcfpq.mongodb.net:27017/user_info?ssl=true&replicaSet=tmega-shard-0&authSource=admin')
    db_website = client.website

    # Post button press to API
    temp_dict = db_website.usrname.find_one({'username':'jwebb'},{'button_one': ()})
    new_value = int(temp_dict['button_one']) + 1
    db_website.usrname.update({'username': 'jwebb'}, {'$set': {'button_one': new_value}}, upsert=False)
    
    # Bedroom Lights (ON)
    if flag == 1:
        b.set_light('lamp 3','on',True)
        b.set_light('lamp 3',{'bri':int(200), 'transitiontime': 1})
        b.set_light('lamp 3','ct',197)

    # Kitchen Lights (ON)
    if flag == 2:
        b.set_group('Kitchen','on',True)
        b.set_group('Kitchen',{'bri':int(100), 'transitiontime': 1})

    # TV (NONE)
    if flag == 3:
        print ("TV 1")

    # Fan (ON)
    if flag == 4:
        env.get_switch('office').on()

    sleep(0.3)

def function_two(flag):
    # Initialization
    env = Environment()
    env.start()
    env.discover(3)
    b = Bridge('192.168.0.100')
    b.connect()
    lights = b.lights
    groups = b.groups
    client = MongoClient('mongodb://tmega:ucsdece188!@tmega-shard-00-00-kcfpq.mongodb.net:27017,tmega-shard-00-01-kcfpq.mongodb.net:27017,tmega-shard-00-02-kcfpq.mongodb.net:27017/user_info?ssl=true&replicaSet=tmega-shard-0&authSource=admin')
    db_website = client.website

    # Post button press to API
    temp_dict = db_website.usrname.find_one({'username':'jwebb'},{'button_two': ()})
    new_value = int(temp_dict['button_two']) + 1
    db_website.usrname.update({'username': 'jwebb'}, {'$set': {'button_two': new_value}}, upsert=False)
    
    # Bedroom Lights (OFF)
    if flag == 1:
        b.set_light('lamp 3','on',False)

    # Kitchen Lights (OFF)
    if flag == 2:
        b.set_group('Kitchen','on',False)

    # TV (NONE)
    if flag == 3:
        print ("TV 2")

    # Fan (OFF)
    if flag == 4:
        env.get_switch('office').off()

    sleep(0.3)

def function_three(flag):
    # Initialization
    env = Environment()
    env.start()
    env.discover(3)
    b = Bridge('192.168.0.100')
    b.connect()
    lights = b.lights
    groups = b.groups
    client = MongoClient('mongodb://tmega:ucsdece188!@tmega-shard-00-00-kcfpq.mongodb.net:27017,tmega-shard-00-01-kcfpq.mongodb.net:27017,tmega-shard-00-02-kcfpq.mongodb.net:27017/user_info?ssl=true&replicaSet=tmega-shard-0&authSource=admin')
    db_website = client.website

    # Post button press to API
    temp_dict = db_website.usrname.find_one({'username':'jwebb'},{'button_three': ()})
    new_value = int(temp_dict['button_three']) + 1
    db_website.usrname.update({'username': 'jwebb'}, {'$set': {'button_three': new_value}}, upsert=False)
    
    # Bedroom Lights (RED)
    if flag == 1:
        b.set_light('lamp 3','xy',[0.675, 0.322])

    # Kitchen Lights (DIM 1)
    if flag == 2:
        b.set_group('Kitchen',{'bri':int(25), 'transitiontime': 1})

    # TV (NONE)
    if flag == 3:
        print ("TV 3")

    # Fan (NONE)
    if flag == 4:
        print ("FAN 3")

    sleep(0.3)
        
if __name__ == '__main__':
    main()
