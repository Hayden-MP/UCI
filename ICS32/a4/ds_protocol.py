# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Hayden Powers
# powersh@uci.edu
# 56169764

# Adaptation of the DSP Protocol

import json
import time


def extract_json(json_msg:str):
  json_dict = {}

  #print("FROM EXTRACT JSON: ", json_msg)
  try:
    json_dict = json.loads(json_msg)   
    token = json_dict['response']['token']
  except json.JSONDecodeError:
    print("Json cannot be decoded.")
    
  return json_dict



