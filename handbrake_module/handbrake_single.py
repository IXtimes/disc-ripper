# General modules
from pyautogui import *
import pyautogui, pyperclip
import time
from datetime import datetime

# Created modules
from utils import clicker, twilio_out, window_management, dvd_driver
from preferences import load_preferences

def rip_single():
    # Get the user's preferences from the preferences file
    preferences = load_preferences.load_preferences()
    
    # Unload preferences into several nammed constants
    EXPORT_PATH = preferences[0]
    RECIPIENT_NUMBERS = preferences[1]
    X_SCALE = (float)(preferences[2])
    Y_SCALE = (float)(preferences[3])
    
    # Store a constant for converting from the first and second window in terms of x position
    # They have the same y, thus this is the only offset needed
    SECOND_WINDOW_OFFSET = 2560 * X_SCALE - 1018
    
    # Store a constant to check if 1 or 2 instances of Handbrake are being used
    INSTANCES = 1
    idle = -1
    
    # Prompt the user if they want to use 1 or 2 instances of Handbrake
    if int(input("How many instances of Handbrake would you like to use? (1/2) ")) == 2:
        INSTANCES = 2
        print("WARNING: Consider suspending PC usage while performing 2 instances of Handbrake to avoid CPU overheating!")
    
    # Prompt the user if they would like to rearrange the Handbrake windows on first time
    if input("Would you like to rearrange the windows in their proper positions? (Y) ").lower()[0] == 'y':
        # Move both Handbrake windows to their specific positions
        instance1_pos = window_management.move_window('Handbrake', 0 * X_SCALE, 310 * Y_SCALE, 0)
        if INSTANCES == 2:
            instance2_pos = window_management.move_window('Handbrake', 0 * X_SCALE + SECOND_WINDOW_OFFSET, 310 * Y_SCALE, 1)
        
    # Program loop
    while True:
        # Check for DVDs if they are avalible in Handbrake
        while len(dvd_driver.get_dvd_drives()) != INSTANCES:
            # Increment an idle timer and animation to show when the program casts polls
            idle += 1
            dots = idle % 3
            if(dots == 0):
                print("Waiting for discs.  ", end='\r')
            if(dots == 1):
                print("Waiting for discs.. ", end='\r')
            if(dots == 2):
                print("Waiting for discs...", end='\r')
            
            # Poll every second
            time.sleep(1)
        
        # Open source options in handbrake
        clicker.rel_click(instance1_pos, 125, 71)
        if INSTANCES == 2:
            clicker.rel_click(instance2_pos, 125, 71)
        
        # Select each DVD option in both instances (if applicable) of handbrake
        clicker.rel_click(instance1_pos, 147, 263)
        if INSTANCES == 2:
            clicker.rel_click(instance2_pos, 147, 318)
            
        time.sleep(1)
        # Poll until either disk is complete (only poll 1 if 2 isnt used)
        job1_complete, job2_complete = False, False
        # Setup encodes
        while not job1_complete or (INSTANCES == 2 and not job2_complete):
            # Encode 1 which is a film
            if not job1_complete and pyautogui.pixel(instance1_pos[0] + 860, instance1_pos[1] + 400)[0] != 64:
                # Disc 1 has loaded
                print(f"Disc 1; has finished scanning! Begining encode...")
                
                # Tab to the subtitle tab
                clicker.rel_click(instance1_pos, 310, 215)
                
                # Clear the subtitles for the film
                print(f"Clearing subtitles for film")
                clicker.rel_click(instance1_pos, 955, 245)
                time.sleep(0.1)
                
                # Fetch the title for the outputted film
                print(f"Fetching film name from {EXPORT_PATH}\\***.mp4")
                clicker.rel_click(instance1_pos, 440, 620)
                pyautogui.hotkey("ctrl", "a")
                pyautogui.hotkey("ctrl", "c")
                path = pyperclip.paste()
                file = path.replace(EXPORT_PATH + '\\', "")
                file = file.replace("_", " ")
                disc1 = file.replace(".mp4", "")
                time.sleep(0.1)
                
                # Push this job to the queue
                clicker.rel_click(instance1_pos, 210, 70)
                
                # Mark this job as now complete
                job1_complete = True
                print(f"Disc 1; {disc1}; has completed assembling, begining encoding process...")
                time.sleep(0.1)
                
                # Perform the encode
                clicker.rel_click(instance1_pos, 345, 70)
            # Encode 2 which is a film
            elif INSTANCES == 2 and not job2_complete and pyautogui.pixel(instance2_pos[0] + 860, instance2_pos[1] + 400)[0] != 64:
                # Disc 1 has loaded
                print(f"Disc 2; has finished scanning! Begining encode...")
                
                # Tab to the subtitle tab
                clicker.rel_click(instance2_pos, 310, 215)
                
                # Clear the subtitles for the film
                print(f"Clearing subtitles for film")
                clicker.rel_click(instance2_pos, 955, 245)
                time.sleep(0.1)
                
                # Fetch the title for the outputted film
                print(f"Fetching film name from {EXPORT_PATH}\\***.mp4")
                clicker.rel_click(instance2_pos, 440, 620)
                pyautogui.hotkey("ctrl", "a")
                pyautogui.hotkey("ctrl", "c")
                path = pyperclip.paste()
                file = path.replace(EXPORT_PATH + '\\', "")
                file = file.replace("_", " ")
                disc2 = file.replace(".mp4", "")
                time.sleep(0.1)
                
                # Push this job to the queue
                clicker.rel_click(instance2_pos, 210, 70)
                
                # Mark this job as now complete
                job2_complete = True
                print(f"Disc 2; {disc2}; has completed assembling, begining encoding process...")
                time.sleep(0.1)
                
                # Perform the encode
                clicker.rel_click(instance2_pos, 345, 70)
            else:
                idle += 1
                dots = idle % 3
                if(dots == 0):
                    print("Scanning discs.  ", end='\r')
                if(dots == 1):
                    print("Scanning discs.. ", end='\r')
                if(dots == 2):
                    print("Scanning discs...", end='\r')
            # Poll every 3 seconds
            time.sleep(3)
        
        # Submit debug
        debugResult = 'Disc encoding task started at: ' + datetime.now().strftime("[%Y-%m-%d] %H:%M:%S") + '\n- # of instances: ' 
        debugResult += str(INSTANCES) + '\n- Disc 1: ' + str(disc1)
        if INSTANCES == 2:
            debugResult += '\n- Disc 2: ' + str(disc2)
        print(debugResult)
        
        # Push update text that a job has begun
        twilio_out.post_to_numbers(debugResult, RECIPIENT_NUMBERS)
        
        # Poll for encode completion
        disc1_encoded, disc2_encoded = False, False
        while not disc1_encoded or (INSTANCES == 2 and not disc2_encoded):
            if not disc1_encoded and pyautogui.pixel(instance1_pos[0] + 301, instance1_pos[1] + 71)[0] != 241:
                time.sleep(10)
                if pyautogui.pixel(instance1_pos[0] + 301, instance1_pos[1] + 71)[0] != 241:
                    disc1_encoded = True
            elif not disc2_encoded and pyautogui.pixel(instance2_pos[0] + 301, instance2_pos[1] + 71)[0] != 241:
                time.sleep(10)
                if pyautogui.pixel(instance2_pos[0] + 301, instance2_pos[1] + 71)[0] != 241:
                    disc2_encoded = True
            else:
                # Increment an idle timer and animation to show when the program casts polls
                idle += 1
                dots = idle % 3
                if(dots == 0):
                    print("Encoding discs.  ", end='\r')
                if(dots == 1):
                    print("Encoding discs.. ", end='\r')
                if(dots == 2):
                    print("Encoding discs...", end='\r')
            # Poll every 3 seconds
            time.sleep(3)
        
        # Push job completion through text
        debugResult = 'Disc ripping task COMPLETED at: ' + datetime.now().strftime("[%Y-%m-%d] %H:%M:%S") + '\n- # of instances: ' 
        debugResult += str(INSTANCES) + '\n- Disc 1: ' + str(disc1)
        if INSTANCES == 2:
            debugResult += '\n- Disc 2: ' + str(disc2)
        print(debugResult)
        twilio_out.post_to_numbers(debugResult, RECIPIENT_NUMBERS)
        
        # Wait for the disc drives to be emptied
        while len(dvd_driver.get_dvd_drives()) != 0:
            # Increment an idle timer and animation to show when the program casts polls
            idle += 1
            dots = idle % 3
            if(dots == 0):
                print("Please empty disc drives!  ", end='\r')
            if(dots == 1):
                print("Please empty disc drives!. ", end='\r')
            if(dots == 2):
                print("Please empty disc drives!..", end='\r')
                
            # Poll every second
            time.sleep(1)
        
        
        