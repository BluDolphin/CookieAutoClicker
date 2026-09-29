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
autoClickDelay = 0.001 # Set auto clicker delay
startStopKey = KeyCode(char='z') # Set key to start/stop
frenzyKey = KeyCode(char='x') # Set key to frenzy
fortuneKey = KeyCode(char='\\') # Set key to fortune click
fortuneNewsDelay = 5 # Set delay for checking for fortune news

boundaryToggle = True # Change to False to disable boundary auto turn off
autoSnapToggle = True # Change to False to disable auto snap to image
frenzyToggle = True # Change to False to disable frenzy click
fortuneAutoClickToggle = True # Change to False to disable auto click on fortune news

# ================================================================================================
# Advanced settings

# Get script directory
programDirectory = os.path.dirname(os.path.abspath(__file__)) # Gcets the directory of the script and passes it to get the directory

# Set the location of the images
# By default the images need to be in the same directory as this program
cookiepath = os.path.join(programDirectory, 'cookie.png')
frenzyPath = os.path.join(programDirectory, 'frenzyCookie.png')
fortunePath = os.path.join(programDirectory, 'fortuneNews.png')

# check if os is not windows
if os.name != 'nt':
    print("Auto snap to image & Frenzy mode is disabled as it is not supported on this OS")
    autoSnapToggle = False
    frenzyToggle = False
    fortuneAutoClickToggle = False
    
# ================================================================================================


mouse = Controller() # Create mouse object
clicking = False # Set clicking to false
frenzy = False # Set frenzy to false
fortuneAutoClick = False # Set fortune auto click to false
pyautogui.PAUSE = 0.01 # Delay for pyautogui between image searches


def find_image_center(image_path, confidence=0.70, grayscale=True):
    location = pyautogui.locateOnScreen(image_path, grayscale=grayscale, confidence=confidence)
    if location is None:
        return None
    return pyautogui.center(location)


def displayStats():
    print("\n\n\n\n\n\n\n\n\n\n")
    print("Auto Clicker Starting\n"
        f"Start/Stop button: {startStopKey}\n"
        f"Frenzy button: {frenzyKey}\n"
        f"Fortune button: {fortuneKey}\n\n"
        
        f"Auto Clicker Delay: {autoClickDelay}\n"
        f"Fortune News Delay: {fortuneNewsDelay}\n\n"
        
        f"Clicking: {clicking}\n"
        f"Frenzy Running: {frenzy}\n"
        f"Fortune Auto Click: {fortuneAutoClick}\n")
displayStats()


# ---------------------------------------------------------


def active(delay): # Function to click
    while clicking == True: # While true
        mouse.click(Button.left) # Click the button
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
                print(f"Auto clicker disabled") # Print the clicking status
                time.sleep(0.1) # Sleep for 0.1 seconds

def fortuneNewsCheck(delay): # Function to check for fortune news
    global clicking
    while fortuneAutoClick == True: # While true
        reactivateClicking = False # Set reactivateClicking to false

        try:
            time.sleep(delay) # Sleep for the delay
            imageLocation = pyautogui.locateOnScreen(fortunePath, grayscale=True, confidence=0.70) # Locate the image on the screenz            
            
            # If clicking is true then set reactivateClicking to true
            if clicking == True:
                reactivateClicking = True 
                
            originalMousePos = pyautogui.position() # Get current mouse pos
            
            pyautogui.moveTo(imageLocation) # Move the mouse to the location
            mouse.click(Button.left) # Click the button
            print("Fortune news clicked") # Print that the fortune news was clicked
            
            pyautogui.moveTo(originalMousePos) # Move the mouse back to the original position
            
            
            # If reactivateClicking is true then set clicking to true
            if reactivateClicking == True: 
                clicking = True
                print(f"Auto clicker re-enabled") # Print the clicking status
                
                # Create thread for active function
                clickingThread = threading.Thread(target=active, args=(autoClickDelay,))
                clickingThread.start()
                
                # Create thread for boundary functionality
                if boundaryToggle == True:
                    boundaryThread = threading.Thread(target=boundary) 
                    boundaryThread.start()

        except Exception as e:
            continue
    return

# ----------------------------czz-----------------------------


def keyLogger(key): # Function for tracking key presses
    global clicking, fortuneAutoClick, frenzy
    
    if key == startStopKey: # If the key pressed is the start/stop key
        try: 
            if autoSnapToggle == True:
                imageLocation = pyautogui.locateOnScreen(cookiepath, grayscale=True, confidence=0.70) # Locate the image on the screen
                imageLocation = (imageLocation[0], imageLocation[1] - 100, imageLocation[2], imageLocation[3]) # modify y to raise the mouse to middle
                pyautogui.moveTo(imageLocation) # Move the mouse to the location 
                clicking = not clicking # Set clicking to the opposite of what it is
            
            if autoSnapToggle == False:    
                clicking = not clicking # Set clicking to the opposite of what it is
            
            
            if clicking == True: # if clicking is true 
                # Create thread for active function
                clickingThread = threading.Thread(target=active, args=(autoClickDelay,))
                clickingThread.start()
                
                if boundaryToggle == True:
                    boundaryThread = threading.Thread(target=boundary) 
                    boundaryThread.start()
            displayStats()
                
        except Exception as e:
            clicking = False
            displayStats()
            
            print(f"Error: {e}")
            print("No cookie found")
            

    
    if key == frenzyKey and frenzyToggle == True: # If the key pressed is the frenzy key
        clicking = False # Set clicking to false to disable if auto clicker is currently running
        frenzy = True # Set frenzy to true
        displayStats()


        while frenzy == True: # While true
            try:
                for pos in pyautogui.locateAllOnScreen(frenzyPath, grayscale=True, confidence=0.8): # Locate all the images on the screen
                    pyautogui.moveTo(pyautogui.center(pos)) # Move the mouse to the center of the image
                    mouse.click(Button.left) # Click the button
                    
            except Exception as e: # Exit on no frenzy cookie found
                print(f"Error: {e}")
                print("No frenzy cookie found") # Print if no cookie is found
                frenzy = False
                displayStats()
                break # Break the loop
    
    if key == fortuneKey and fortuneAutoClickToggle == True: # If the key pressed is the fortune toggle is enabled
        fortuneAutoClick = not fortuneAutoClick # flip fortune toggle
        
        # if fortuneAutoClick is true 
        if fortuneAutoClick == True:
            fortuneNewsThread = threading.Thread(target=fortuneNewsCheck, args=(fortuneNewsDelay,)) # create thread to check for news
            fortuneNewsThread.start()
            
        displayStats()
        

# Create listener for key logging and start keyLogger function
with Listener(on_press=keyLogger) as listener:
    listener.join() 