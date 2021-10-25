# input_processor.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries
# in Python

# Replace the following placeholders with your information.

# Hayden Powers
# powersh@uci.edu
# 56169764

import input_processor
from Profile import Profile
import sys
from pathlib import Path


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
        create_profile() 
        
    elif(choice == "2"):
        open_profile()

    elif(choice.upper() == "Q"):
        sys.exit()
        
    else:
        print("\nPlease choose a valid option\n")
        start()

    profile_actions()
    return


# Once the profile has been created, we can now edit the contents
def profile_actions():
    global admin

    if(admin):
        return
    
    print("\nWhat would you like to do with your Profile?")
    print("Enter the number based on your choice:\n")
    print("1 - Create another Profile")
    print("2 - Open a different Profile")
    print("3 - Edit Profile")
    print("4 - Edit Posts")
    print("5 - Show Profile information\n")

    choice = input()

    if(choice == 'admin'):
        admin = True
        print("\n** admin mode activated **\n")
        return
        
    elif(choice == "1"):
        create_profile()
        profile_actions()
        
    elif(choice == "2"):
        open_profile()
        profile_actions()
        
    elif(choice == "3"):
        edit_profile()
        profile_actions()

    elif(choice == "4"):
        edit_posts()
        profile_actions()

    elif(choice == "5"):
        print_profile()
        profile_actions()

    elif(choice.upper() == "Q"):
        sys.exit()
        
    else:
        print("\nPlease choose a valid option\n")
        profile_actions()

    return


# This method will print/display any information in a Profile,
# using the P command in input_processor
def print_profile():
    global admin
    
    print("\nWhat would you like to show in your Profile?")
    print("Enter the number based on your choice:\n")
    print("1 - Username")
    print("2 - Password")
    print("3 - Bio")
    print("4 - Specific Post")
    print("5 - All Posts")
    print("6 - Everything")

    choice = input()

    if(choice == 'admin'):
        admin = True
        print("\n** admin mode activated **\n")
        return
        
    elif(choice == "1"):
        print("Current username: ")
        input_processor.process_input("P -usr ")

    elif(choice == "2"):
        print("Current password: ")
        input_processor.process_input("P -pwd ")
        
    elif(choice == "3"):
        print("Current bio: ")
        input_processor.process_input("P -bio ")

    elif(choice == "4"):
        try:
            post = input("Enter the ID number for the post: ")
            input_processor.process_input("P -post " + post + " ")
        except TypeError:
            print("\nPlease only enter an integer value for the ID")
            print_profile()
        
    elif(choice == "5"):
        print("All posts: ")
        input_processor.process_input("P -posts ")
        
    elif(choice == "6"):
        print("All info: ")
        input_processor.process_input("P -all ")

    elif(choice.upper() == "Q"):
        sys.exit()
        
    else:
        print("\nPlease choose a valid option\n")
        print_profile()

    return

    
# This method will be able to change any information in a Profile,
# using the E command in input_processor
def edit_profile():
    global admin
    
    print("\nWhat would you like to change in your Profile?")
    print("Enter the number based on your choice:\n")
    print("1 - Username")
    print("2 - Password")
    print("3 - Bio")

    choice = input()

    if(choice == 'admin'):
        admin = True
        print("\n** admin mode activated **\n")
        return
        
    elif(choice == "1"):
        username = input("\nPlease enter your new username: ")
        input_processor.process_input(f"E -usr \"{username}\"")

    elif(choice == "2"):
        password = input("\nPlease enter your new password: ")
        input_processor.process_input(f"E -pwd \"{password}\"")
        
    elif(choice == "3"):
        bio = input("\nPlease enter your new bio: ")
        input_processor.process_input(f"E -bio \"{bio}\"")

    elif(choice.upper() == "Q"):
        sys.exit()
        
    else:
        print("\nPlease choose a valid option\n")
        profile_actions()

    return


def edit_posts():
    global admin
    print("\nPlease choose a numbered option: ")
    print("1 - Add post")
    print("2 - Delete post")

    choice = input()

    if(choice == 'admin'):
        admin = True
        print("\n** admin mode activated **\n")
        return
        
    elif(choice == "1"):
        post = input("\nPlease enter your new post: ")
        input_processor.process_input("E -addpost " + post + " ")
        print("Post added: ", post)


    elif(choice == "2"):
        print("\nAll posts: ")
        input_processor.process_input("P -posts ")
        print("\nPlease enter the number of your post to delete it:")
        try:
            post_index = input()
            input_processor.process_input(f"E -delpost " + post_index + " ")
        except TypeError:
            print("Only enter an integer value associated with the post.")
            edit_posts()
        
    elif(choice.upper() == "Q"):
        sys.exit()
        
    else:
        print("\nPlease choose a valid option\n")
        profile_actions()


# This method will use methods in input_processor to create a profile
def create_profile():
    print("Please enter the following fields to create a Profile:")
    path = input("Path to store profile: ")

    if(valid_path(path)):    
        name = input("\nName of Profile: ")
        input_processor.process_input(f"C {path} -n {name} ") 
        print("\nProfile created")


# This method will use methods in input_processor to open a profile
def open_profile():
    print("\nPlease enter the path where your profile is stored.")
    path = input("Path: ")
    if(valid_path(path)):    
        input_processor.process_input("O " + path + " ")
    
    
# This method will facilitate admin mode
def admin_mode():
    global admin
    usr_input = input()
    if(usr_input == "admin"):
        admin = False
        print("\n** admin mode deactivated **\n")
    else:
        input_processor.process_input(usr_input+" ")



# Method that validates the path to use in different methods
def valid_path(path: str) -> bool:
    if(Path(path).exists()):
        return True
    input_processor.error()
    return False


# Loop
while True:
    while admin:
        admin_mode()
    start()
