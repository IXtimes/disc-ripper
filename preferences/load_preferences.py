import os
import sys
import tkinter as tk

# Determines the execution's directory to determine where to look for a preferences file
def get_executable_directory():
    # Determine if the script is ran as an executable or from a python file
    if getattr(sys, 'frozen', False):
        # Get the executable from sys
        return os.path.abspath(os.path.dirname(sys.executable))
    else:
        # Get the ran file directory
        return os.path.abspath(os.path.dirname(__file__))
    
# Loads values from the preferences file created in the same directory
def load_preferences():
    # Create an empty preferences reference
    preferences = []
    
    # Get the preferences file path
    preferences_file = os.path.join(get_executable_directory(), 'pref.ini')
    
    # Determine if a preferences file exists
    if os.path.exists(preferences_file):
        # Process the lines of the preferences file
        with open(preferences_file, 'r') as file:
            for line in file:
                # Add the value of each preference as they occur
                preference = line.split(':', 1)
                
                # Strip whitespace characters
                preference[1] = preference[1].strip()
                
                # Check if the specified preference is a list of values
                if ',' in preference[1]:
                    # Create a list splitting by the comma
                    sub_preferences = preference[1].split(',')
                    
                    # Append the list of preferences
                    preferences.append(sub_preferences)
                else:
                    preferences.append(preference[1])
    else:
        # Create a preferences file in the directory
        with open(preferences_file, 'a') as file:
            # Get the root to find screen resolution
            root = tk.Tk()
            
            # Append perference fields for export path
            file.write("Export Path: *enter handbrake export path here*\n")
            file.write("Recipient Numbers: *enter comma seperated list of recipient numbers here*\n")
            file.write(f"X Scale Factor: {root.winfo_screenwidth() / 2560}\n")
            file.write(f"Y Scale Factor: {root.winfo_screenheight() / 1440}")
            file.write("Twilio Account SID: *enter SID here*\n")
            file.write("Twilio Auth. Token: *enter auth. token here*\n")
            file.write("Twilio Bot Number: *enter the phone number associated with the twilio bot here*\n")
        print("Preferences file did not exist in directory, creating one now!")
        sys.exit()
    
    # Return the intercepted preferences
    return preferences