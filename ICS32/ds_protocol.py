# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Hayden Powers
# powersh@uci.edu
# 56169764

# Adaptation of the DSP Protocol

import json
from collections import namedtuple
import time


def extract_json(json_msg:str):
  json_dict = {}
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  
  TODO: replace the pseudo placeholder keys with actual DSP protocol keys
  '''
  print("FROM EXTRACT JSON: ", json_msg)
  try:
    json_dict = json.loads(json_msg)   
    token = json_dict['response']['token']
  except json.JSONDecodeError:
    print("Json cannot be decoded.")
    
  return json_dict


  

# NOTES:
'''
- JSON objects are just dictionaries
- The token variable is an identifier of the user
- UI that says : DO you want to create a profile? (join)
                Do you want to make a post? (post)
                Do you want to make a bio? (bio)

'''
