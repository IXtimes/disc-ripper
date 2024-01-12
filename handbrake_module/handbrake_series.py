# General modules
from pyautogui import *
import pyautogui
import time
from datetime import datetime

# Created modules
from utils import clicker, twilio_out, window_management, dvd_driver
from preferences import load_preferences
    
def rip_series():
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
        
        # Get specifics about disc titles, episode ranges, etc
        disc1 = input("Enter the title for the first disc: ")
        if INSTANCES == 2:
            if input("Would you like to reuse this title for disk 2? (Y) ").lower()[0] == 'y':
                disc2 = disc1
            else:
                disc2 = input("Enter the title for the second disc: ")
        ep_range = input(f"Enter the episode range for {disc1} (disc 1): (X-Y) ")
        split_range = ep_range.split('-')
        disk1_range_min, disk1_range_max = int(split_range[0]), int(split_range[1])
        if INSTANCES == 2:
            ep_range = input(f"Enter the episode range for {disc2} (disc 2): (X-Y) ")
            split_range = ep_range.split('-')
            disk2_range_min, disk2_range_max = int(split_range[0]), int(split_range[1])
        start_title1 = int(input(f"Enter the title number to start rip 1 at (an offset, not literal): "))
        if INSTANCES == 2:
            start_title2 = int(input(f"Enter the title number to start rip 2 at (an offset, not literal): "))
             
        # Submit debug
        debugResult = 'Disc ripping task started at: ' + datetime.now().strftime("[%Y-%m-%d] %H:%M:%S") + '\n- # of instances: ' 
        debugResult += str(INSTANCES) + '\n- Disc 1: ' + str(disc1)
        debugResult += '['+ str(disk1_range_min) + '-' + str(disk1_range_max) +']'
        if INSTANCES == 2:
            debugResult += '\n- Disc 2: ' + str(disc2)
            debugResult += '['+ str(disk2_range_min) + '-' + str(disk2_range_max) +']'
        print(debugResult)
        # Push update text that a job has begun
        twilio_out.post_to_numbers(debugResult, RECIPIENT_NUMBERS)
        
        # Poll until either disk is complete (only poll 1 if 2 isnt used)
        job1_complete, job2_complete = False, False
        idle = -1
        # Setup encodes
        while not job1_complete or (INSTANCES == 2 and not job2_complete):
            # Encode 1 when its done processing the disc
            if not job1_complete and pyautogui.pixel(instance1_pos[0] + 860, instance1_pos[1] + 400)[0] != 64:
                # Disc 1 has loaded
                print(f"Disc 1; {disc1}; has finished scanning! Processing episodes...")
                
                # Tab to the subtitle tab
                clicker.rel_click(instance1_pos, 310, 215)
                
                # Keep an offset handy
                offset = (163 + ((start_title1 - 1) * 17))
                
                # Iterate through the number of episode jobs to create
                j = 0
                for i in range(disk1_range_min, disk1_range_max + 1):
                    j += 1
                    # Perform the operations to add a episode to the queue
                    # Get the correct episode title
                    print(f"Fetching title {start_title1 + j}")
                    clicker.rel_click(instance1_pos, 155, 146)
                    time.sleep(0.1)
                    clicker.rel_scroll(instance1_pos, 155, offset)
                    time.sleep(0.1)
                    clicker.rel_click(instance1_pos, 245, offset)
                    offset += 17
                    time.sleep(0.1)
                    
                    # Clear the subtitles for the episode
                    print(f"Clearing subtitles for title {i}")
                    clicker.rel_click(instance1_pos, 955, 245)
                    time.sleep(0.1)
                    
                    # Write the title for the outputted episode
                    print(f"Renaming title {i} to {EXPORT_PATH}\\{disc1} E{i}.mp4")
                    clicker.rel_click(instance1_pos, 440, 620)
                    pyautogui.hotkey("ctrl", "a")
                    pyautogui.press("backspace")
                    pyautogui.typewrite(f"{EXPORT_PATH}\\{disc1} E{i}.mp4")
                    time.sleep(0.1)
                    
                    # Push this job to the queue
                    clicker.rel_click(instance1_pos, 210, 70)
                
                # Mark this job as now complete
                job1_complete = True
                print(f"Disc 1; {disc1}; has completed assembling episodes, begining encoding process...")
                time.sleep(0.1)
                
                # Perform the encode
                clicker.rel_click(instance1_pos, 345, 70)
            # Encode 2 when its done processing scanning the disc
            elif INSTANCES == 2 and (not job2_complete and pyautogui.pixel(instance2_pos[0] + 860, instance2_pos[1] + 400)[0] != 64):
                # Disc 1 has loaded
                print(f"Disc 2; {disc2}; has finished scanning! Processing episodes...")
                
                # Tab to the subtitle tab
                clicker.rel_click(instance2_pos, 310, 215)
                
                # Keep an offset handy
                offset = (163 + ((start_title2 - 1) * 17))
                
                # Iterate through the number of episode jobs to create
                j = 0
                for i in range(disk2_range_min, disk2_range_max + 1):
                    j += 1
                    # Perform the operations to add a episode to the queue
                    # Get the correct episode title
                    print(f"Fetching title {i}")
                    clicker.rel_click(instance2_pos, 155, 146)
                    time.sleep(0.1)
                    clicker.rel_scroll(instance2_pos, 155, offset)
                    time.sleep(0.1)
                    clicker.rel_click(instance2_pos, 245, offset)
                    offset += 17
                    time.sleep(0.1)
                    
                    # Clear the subtitles for the episode
                    print(f"Clearing subtitles for title {i}")
                    clicker.rel_click(instance2_pos, 955, 245)
                    time.sleep(0.1)
                    
                    # Write the title for the outputted episode
                    print(f"Renaming title {i} to {EXPORT_PATH}\\{disc2} E{i}.mp4")
                    clicker.rel_click(instance2_pos, 440, 620)
                    pyautogui.hotkey("ctrl", "a")
                    pyautogui.press("backspace")
                    pyautogui.typewrite(f"{EXPORT_PATH}\\{disc2} E{i}.mp4")
                    time.sleep(0.1)
                    
                    # Push this job to the queue
                    clicker.rel_click(instance2_pos, 210, 70)
                
                # Mark this job as now complete
                job2_complete = True
                print(f"Disc 2; {disc2}; has completed assembling episodes, begining encoding process...")
                time.sleep(0.1)
                
                # Perform the encode
                clicker.rel_click(instance2_pos, 345, 70)
            else:
                # Increment an idle timer and animation to show when the program casts polls
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
        debugResult += '['+ str(disk1_range_min) + '-' + str(disk1_range_max) +']'
        if INSTANCES == 2:
            debugResult += '\n- Disc 2: ' + str(disc2)
            debugResult += '['+ str(disk2_range_min) + '-' + str(disk2_range_max) +']'
        print(debugResult)
        twilio_out.post_to_numbers(debugResult, RECIPIENT_NUMBERS)
        
        # Request repeat
        # Wait for the disc drives to be emptied
        while len(dvd_driver.get_dvd_drives()) != 0:
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
        
        