from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import time, threading, os, pyautogui

"""_summary_
Auto clicker script with boundary check

Features:
- Clicks fast
- Stops clicking when mouse is outside of a boundary
- Automatically moves mouse to image location (Winodws only)
- Can auto find and click on many images (Windows only)
"""


# ================================================================================================
# SETTINGS
delay = 0.001 # Set delay
button = Button.left # Set button to press
startStopKey = KeyCode(char='z') # Set key to start/stop
frenzyKey = KeyCode(char='x') # Set key to frenzy

boundaryToggle = True # Change to False to disable boundary auto turn off
autoSnapToggle = True # Change to False to disable auto snap to image
frenzyToggle = True # Change to False to disable frenzy click

# ================================================================================================
# Advanced settings

# Get script directory
programDirectory = os.path.dirname(os.path.abspath(__file__)) # Gets the directory of the script and passes it to get the directory

# Set the location of the images
# By default the images need to be in the same directory as this program
cookiepath = os.path.join(programDirectory, 'cookie.png')
frenzyPath = os.path.join(programDirectory, 'frenzyCookie.png')

# ================================================================================================
print("Auto Clicker Starting\n"
      f"Delay: {delay: 0.001}\n"
      f"Auto click button: {button}\n"
      f"Start/Stop button: {startStopKey}\n"
      f"Frenzy button: {frenzyKey}\n")

# check if os is not windows
# Auto disable features if not supported on Linux (probs MacOS too
if os.name != 'nt':
    print("Auto snap to image & Frenzy mode is disabled as it is not supported on this OS z\nSorry, i'm working on implementing it currently")
    autoSnapToggle = False
    frenzyToggle = False

mouse = Controller() # Create mouse object
clicking = False # Set clicking to false
frenzy = False # Set frenzy to false
pyautogui.PAUSE = 0.01 # Delay for pyautogui between image searches

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
        try: 
            if autoSnapToggle == True:
                imageLocation = pyautogui.locateOnScreen(cookiepath, grayscale=True, confidence=0.70) # Locate the image on the screen
                imageLocation = (imageLocation[0], imageLocation[1] - 100, imageLocation[2], imageLocation[3]) # modify y to raise the mouse to middle
                pyautogui.moveTo(imageLocation) # Move the mouse to the location 
                clicking = not clicking # Set clicking to the opposite of what it is
                print (f"Auto clicker: {clicking}") # Print the key pressed
            
            if autoSnapToggle == False:    
                clicking = not clicking # Set clicking to the opposite of what it is
                print (f"Auto clicker: {clicking}") # Print the key pressed
            
            
            if clicking == True: # if clicking is true 
                # Create thread for active function
                clickingThread = threading.Thread(target=active, args=(delay, button))
                clickingThread.start()
                
                if boundaryToggle == True:
                    boundaryThread = threading.Thread(target=boundary) 
                    boundaryThread.start()
                
        except Exception as e:
            print(f"Error: {e}")
            print("No cookie found")
            clicking = False
    
    if key == frenzyKey and frenzyToggle == True: # If the key pressed is the frenzy key
        print("Frenzy mode: On") # Print frenzy mode is true
        clicking = False # Set clicking to false to disable if auto clicker is currently running
        frenzy = True # Set frenzy to true

        while frenzy == True: # While true
            try:
                for pos in pyautogui.locateAllOnScreen(frenzyPath, grayscale=True, confidence=0.8): # Locate all the images on the screen
                    pyautogui.moveTo(pos) # Move the mouse to the location
                    mouse.click(Button.left) # Click the button
                    
            except Exception as e: # Exit on no frenzy cookie found
                print(f"Error: {e}")
                print("No frenzy cookie found") # Print if no cookie is found
                frenzy = False
                break # Break the loop

# Create listener for key logging and start keyLogger function
with Listener(on_press=keyLogger) as listener:
    listener.join() 