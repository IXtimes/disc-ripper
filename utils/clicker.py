from pyautogui import *
from typing import Tuple
import pyautogui

# Performs a mouse click at the passed x and y screen coordinates
def click(x, y):
    # Move the mouse cursor to the x, y coordinates specified
    pyautogui.moveTo(x, y)
    
    # Perform a mouse click at said position
    pyautogui.click()

# Performs a mouse click relative to the coordinates specified
def rel_click(basis: Tuple[int, int], x, y):
    # Move the mouse cursor to the x, y coordinate offset from w, v
    pyautogui.moveTo(basis[0] + x, basis[1] + y)
    
    # Perform a mouse click at said position
    pyautogui.click()
    
# Scrolls the mouse wheel at the position specifed the number of times specified in the direction denoted
def scroll(x, y, n = 5, dir = 1):
    # Move the mouse cursor to the x, y coordinate
    pyautogui.moveTo(x, y)
    
    # Release the action delay between pyautogui actions
    pyautogui.PAUSE = 0.01
    
    # Iterate the scroll action n times
    for i in range(n):
        # Scroll 100 units in the direction specified
        pyautogui.scroll(100 * dir)
    
    # Reset the action delay between pyautogui actions
    pyautogui.PAUSE = 0.1
    
# Scrolls the mouse wheel at the position specifed the number of times specified in the direction denoted
def rel_scroll(basis: Tuple[int, int], x, y, n = 5, dir = 1):
    # Move the mouse cursor to the x, y coordinate
    pyautogui.moveTo(basis[0] + x, basis[1] + y)
    
    # Release the action delay between pyautogui actions
    pyautogui.PAUSE = 0.01
    
    # Iterate the scroll action n times
    for i in range(n):
        # Scroll 100 units in the direction specified
        pyautogui.scroll(100 * dir)
    
    # Reset the action delay between pyautogui actions
    pyautogui.PAUSE = 0.1