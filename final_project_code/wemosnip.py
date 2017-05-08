# Imports needed
import ouimeaux
from ouimeaux.environment import Environment

# Initialization
env = Environment()

# Start environment
env.start()

# Discover devices w/ time in seconds
env.discover(3)

# Turn off switch
env.get_switch('office').off()

# Turn on switch
env.get_switch('office').on()
