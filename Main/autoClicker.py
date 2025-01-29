from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import time, threading, os, pyautogui

"""_summary_
Auto clicker script with boundary check

Features:
- Clicks fast
- Stops clicking when mouse is outside of a boundary
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

def boundary(): # Function to check if the mouse is in the boundary+
    global clicking
    mouseCenterPos = pyautogui.position() # Get the mouse position
    rangeXY = (50, 50) # Set tuple for boundary range (x, y)

    # Boundary works using x and y co-ords as invisible lines 
    # If the mouse goes past the line then its outside of the box
    boundary = (mouseCenterPos[0] - rangeXY[0], # Left X line
                mouseCenterPos[0] + rangeXY[0], # right X Line
                mouseCenterPos[1] - rangeXY[1], # left Y Line
                mouseCenterPos[1] + rangeXY[1]) # right Y line

    while clicking == True: # While clicking is true
        mousePosition = pyautogui.position()
        if  not (boundary[0] < mousePosition[0] < boundary[1] and # If the mouse is winthin the x range
                 boundary[2] < mousePosition[1] < boundary[3]): # If the mouse is within the y range
                
                clicking = False # If the mouse is outside of the range then set clicking to false
                print(f"Auto clicker: {clicking}") # Print the clicking status
                time.sleep(0.1) # Sleep for 0.1 seconds


def keyLogger(key): # Function for tracking key presses
    global clicking 
    if key == startStopKey: # If the key pressed is the start/stop key
        clicking = not clicking # Set clicking to the opposite of what it is
        print (f"Auto clicker: {clicking}") # Print the key pressed
    
    if clicking == True: # if clicking is true 
        # Create thread for active function
        clickingThread = threading.Thread(target=active, args=(delay, button))
        boundaryThread = threading.Thread(target=boundary) 
        clickingThread.start()
        boundaryThread.start()

# Create listener for key logging
with Listener(on_press=keyLogger) as listener:
    listener.join() 