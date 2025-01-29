from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import time, threading, os

"""_summary_
Simplest auto clicker script

Features:
- Clicks fast
"""

# ================================================================================================
# SETTINGS

delay = 0.001 # Set delay
button = Button.left # Set button to press
startStopKey = KeyCode(char='z') # Set key to start/stop

print("Auto Clicker Starting\n"
      f"Delay: {delay}\n"
      f"Auto click button: {button}\n"
      f"Start/Stop button: {startStopKey}")

mouse = Controller() # Create mouse object
clicking = False # Set clicking to false


# ================================================================================================
# Advanced settings

# Get script directory
programDirectory = os.path.dirname(os.path.abspath(__file__)) # Gets the directory of the script and passes it to get the directory

# Set the location of the images
# By default the images need to be in the same directory as this program
cookiepath = os.path.join(programDirectory, 'cookie.png')
frenzyPath = os.path.join(programDirectory, 'frenzyCookie.png')

# ================================================================================================
def active(delay, button): # Function to click
    while clicking == True: # While true
        mouse.click(button) # Click the button
        time.sleep(delay) # Sleep for the delay
    return

def keyLogger(key): # Function for tracking key presses
    global clicking 
    if key == startStopKey: # If the key pressed is the start/stop key
        clicking = not clicking # Set clicking to the opposite of what it is
        print (f"Auto clicker: {clicking}") # Print the key pressed
    
    if clicking == True: # if clicking is true 
        # Create thread for active function
        clickingThread = threading.Thread(target=active, args=(delay, button)) 
        clickingThread.start()

# Create listener for key logging
with Listener(on_press=keyLogger) as listener:
    listener.join() 