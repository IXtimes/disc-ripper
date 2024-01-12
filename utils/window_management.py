from pyautogui import *
import pyautogui, pygetwindow
import win32gui
import time

# (UTLITY)
# Gets the window title at the current mouse position
def get_window_title():
    # Use a try-catch statement to ensure program stablity
    try:
        # Get the mouse position's x and y position
        x, y = pyautogui.position()
        
        # Get window found at a tuple constructed at those coordinates
        window = win32gui.WindowFromPoint((x, y))
        
        # Get the title of the window as a string
        title = win32gui.GetWindowText(window)
        
        # Return the title
        return title
    except Exception as e:
        # Report any error encountered
        print(f"Error {e}")
        
        # Terminate
        return None
    
# Moves the window specfied by title (and possibly index) to the targeted screen coordinates
def move_window(window_title, target_x, target_y, index = 0):
    # Use a try-catch statement to ensure program stability
    try:
        # Fetch all (if any) windows of the name passed into the function
        windows = pygetwindow.getWindowsWithTitle(window_title)
        
        # Check if any windows were found with the specified name at all
        if not windows:
            # Report such case
            print(f"No windows found with the title: '{window_title}'.")
            
            # Terminate
            return
        
        # Get the specific window at the index specified
        target_window = windows[index]
        
        # Move the position specified
        target_window.moveTo((int)(target_x), (int)(target_y))
        print(f"Moved '{window_title}, instance: {index}, to the coordinates ({target_x}, {target_y})")
        
        # Return the coordinates that the window was moved to
        time.sleep(0.01)
        return ((int)(target_x), (int)(target_y))
    except Exception as e:
        # Report any error encountered
        print(f"Error {e}")
        
        # Terminate
        return None