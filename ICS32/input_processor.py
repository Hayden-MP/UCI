# input_processor.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries
# in Python

# Replace the following placeholders with your information.

# Hayden Powers
# powersh@uci.edu
# 56169764

# Input processor will be the module that controls the UI

import a2


admin = False

# Start will call all other methods in this module
def start():
    global admin
    while admin:
        admin_mode()
        
    print("\nWelcome to your Journal\n")
    print("Please select an option below using the number associated with")
    print("your choice or enter Q to exit any time:\n")
    print("1 - I want to Create a Profile")
    print("2 - I want to Open a Profile\n")

    choice = input()
    
    if(choice == 'admin'):
        admin = True
        print("\n** admin mode activated **\n")
        return
        
    elif(choice == "1"):
        print("\nYou picked CREATE A PROFILE")
        
    elif(choice == "2"):
        print("\nYou picked OPEN A PROFILE")
        
    else:
        print("\nPlease choose a valid option\n")


def create_profile():
    pass

def open_profile():
    pass

# This method will facilitate admin mode
def admin_mode():
    global admin
    usr_input = input()
    if(usr_input == "admin"):
        admin = False
        print("\n** admin mode deactivated **\n")
    else:
        a2.process_input(usr_input+" ")


# Our loop
while True:
    start()
