# a3.py

# Starter code for assignment 3 in ICS 32 Programming with Software
# Libraries in Python

# Replace the following placeholders with your information.

# Hayden Powers
# powersh@uci.edu
# 56169764

import ds_client
import json
from pathlib import Path
import input_processor
import sys

HOST, profile_path = "", ""
PORT = 3021 # Hard-coded port


def start():
    global HOST, profile_path

    # Welcome - getting/creating profile and HOST information
    print("\nWelcome to the Online Posting System")
    print("Please enter the number associated with your choice:\n")
    print("1 -- Create Profile")
    print("2 -- Load Profile")
    print("3 -- Quit Program\n")

    choice = input().strip()

    if choice == '1':

        # CREATE PROFILE
        path = input("Please enter the path you wish to save your profile: ").strip()
        if not Path(path).exists():
            print("Invalid path! Please try again.")
            start()

        name = input("Please enter the name for the file: ").strip()

        if name != '':
            query = ['C', path, '-n', name]
            profile_path = input_processor.c_command(query)

        else:
            print("Name cannot be empty!")
            start()
    
    elif choice == '2':

        # LOAD PROFILE
        profile_path = input("Enter the path to your dsu file: ").strip()

        if not Path(profile_path).exists and Path(profile_path).suffix != '.dsu':
            print("Profile path is invalid! Please try again.")
            start()

        input_processor.process_input("O " + profile_path + " ")

    elif choice == '3':

        # QUIT PROGRAM
        sys.exit()
    
    else:
        print("Please enter a valid option from the menu!")
        start()

    process_posts()
    start() # Restart method
    
    

# This function will facilitate the creation/loading of posts to save
# locally, post online, or choose an existing post in the dsu file to
# post online
def process_posts():

    global HOST, profile_path
    
    # Access contents of dsu file and convert to dictionary for easy
    # access through python dictionary
    dsu = ""
    try:
        with open(Path(profile_path)) as f:
            dsu = f.read()
            
    except FileNotFoundError as e:
        print("File not found! Please check your path.")
        return

    try:
        json_dsu = json.loads(dsu)
    except json.JSONDecodeError as e:
        print("Issue with DSU file, try again!")
        return
    
    # Create/load/save posts and post online processing
    print(f"\nWelcome {json_dsu['username']}!\n")
    print("Please enter the number associated with your choice:")
    print("Press any other key to go back to start menu\n")
    print("1 -- Create a post")
    print("2 -- List posts")
    print("3 -- Send post to server")
    print("4 -- Update bio online\n")
    choice = input().strip()
    
    if choice == '1':

        # CREATE A POST
        print("Start typing your post and press enter to submit:\n")
        post = input().strip()
        input_processor.process_input("E -addpost " + f'"{post}"' + " ")
        print("Post added: ", post)
        process_posts()

    elif choice == '2':

        # LIST POSTS
        input_processor.process_input("P -posts " + " ")
        process_posts()

    elif choice == '3':

        # SEND POST TO SERVER
        HOST = input("Enter the IP address of your server: ")
        post_index = input("Enter the index number of the post you would like to send: ").strip()
        json_dsu['dsuserver'] = HOST

        query = ['P', '-post', post_index]

        try:
            post = input_processor.post_option(query, int(post_index))['entry']
        
            ds_client.send(json_dsu['dsuserver'], PORT,
                   username=json_dsu['username'],
                   password=json_dsu['password'],
                   message=post,
                   bio=json_dsu['bio'])
            
        except (TypeError, ValueError) as e:
            print("Invalid post option, check your index!")
        
        process_posts()

    elif choice == '4':

        # UPDATE BIO AND SEND
        HOST = input("Enter the IP address of your server: ")
        print("Enter below your updated bio: ")

        updated_bio = input().strip()
        
        json_dsu['bio'] = updated_bio
        json_dsu['dsuserver'] = HOST
        
        query = ['E', '-bio', f'"{updated_bio}"']
        input_processor.bio_option(query, query[0], query[2])
        
        ds_client.send(json_dsu['dsuserver'], PORT,
               username=json_dsu['username'],
               password=json_dsu['password'],
               message="",
               bio=json_dsu['bio'])
        
        process_posts()
    
    else:
        print("\nReturning to start menu...\n")
        return


while True:
    start()
    
