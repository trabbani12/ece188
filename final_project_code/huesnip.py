# Imports needed
from phue import Bridge

# Initialization (done once)
b = Bridge('192.168.0.100') #Define a bridge
b.connect()                 #Link to bridge
lights = b.lights           #Create array of existing lights
groups = b.groups           #Create array of existing groups



###### Kitchen Snippets ######

# Function 1 (Turn on)
#b.set_group('Kitchen','on',True)
#b.set_group('Kitchen',{'bri':int(100), 'transitiontime': 1})

# Function 2 (Turn off)
#b.set_group('Kitchen','on',False)

# Function 3 (Dim Low)
#b.set_group('Kitchen',{'bri':int(25), 'transitiontime': 1})

# Function 4 (Dim Med)
#b.set_group('Kitchen',{'bri':int(50), 'transitiontime': 1})

# Function 5 (Dim High)
#b.set_group('Kitchen',{'bri':int(75), 'transitiontime': 1})

###### Bedroom Snippets ######

# Function 1 (Turn on)
#b.set_light('lamp 3','on',True)
#b.set_light('lamp 3',{'bri':int(200), 'transitiontime': 1})
#b.set_light('lamp 3','ct',197)

# Function 2 (Turn off)
#b.set_light('lamp 3','on',False)

# Function 3 (Dim Low)
#b.set_light('lamp 3',{'bri':int(25), 'transitiontime': 1})
#b.set_light('lamp 3','ct',197)

# Function 4 (Dim Med)
#b.set_light('lamp 3',{'bri':int(50), 'transitiontime': 1})
#b.set_light('lamp 3','ct',197)

# Function 5 (Dim High)
#b.set_light('lamp 3',{'bri':int(100), 'transitiontime': 1})
#b.set_light('lamp 3','ct',197)

# Function 6 (Red)
#b.set_light('lamp 3','xy',[0.675, 0.322])
