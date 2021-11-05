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
from Profile import Profile

HOST = ""
PORT = 3021


# Create the UI to:
#       1. Access post via username/password
#       2. Let user pick a post/enter new post to put online
#       3. This wont let you create a new profile, so the dsu
#           must exist already



# Attempt to open a DSU file to extract information
file = input("Enter path to dsu file: ")
contents = ""

# Open the path  and load into str contents variable
with open(Path(file)) as f:
    contents = f.read()

# Convert to json for easy access
json_obj = json.loads(contents)
print(json_obj)

# Set value HOST to dsuserver key, will use UI to allow user to change later
json_obj['dsuserver'] = HOST
print(json_obj)


# Successful send
ds_client.send(json_obj['dsuserver'], PORT,
               username=json_obj['username'],
               password=json_obj['password'],
               message="message",
               bio=json_obj['bio'])

#ds_client.send(HOST, PORT, username="meow", password="pwd123", message="yeeeuhh get into it", bio="iam the best meow")


    
# QUESTIONS FOR TA:
'''
- Are we passing in profile object to extract username/password/bio/etc?
- Does a3 have a UI or is that separate? (grading criteria)
- If UI, do we use our a2 to be able to create profile objects or are we
    JUST accessing them?
- where do we handle exceptions? in protocol?
- Do we post ALL posts to the server or just the most recent? If a dsu file has multiple posts for example
    and hasnt posted online before, do we post all of them? How do we check that they havent posted the same
    list twice?

    Also, why is posts considered private? "_posts"? 
'''
