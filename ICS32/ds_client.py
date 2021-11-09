# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Hayden Powers
# powersh@uci.edu
# 56169764

#  This is the distributed social client module. It contains all code required
#  to exchange messages with the DSP Server

import socket
import ds_protocol
import json
import time


# Send function sends the dsu file information to the DSP server
def send(server:str, port:int, username:str, password:str, message:str, bio:str=None):

  if not valid_ip(server): # If valid_ip returns FALSE, run this 
    print("Invalid IP! Try again.")
    return
  
  HOST = server
  PORT = port

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:

    json_dict = join(HOST, PORT, client, username, password)
    check_errors(json_dict)

    post_response = post(json_dict, client, message)
    check_errors(post_response)

    if bio != None:
      bio_response = bio_post(json_dict, client, bio)
      check_errors(bio_response)



# Function to facilitate joining the server
def join(HOST, PORT, client, username, password):
  # Connect to our server here
  try:
    client.connect((HOST, PORT))
    
  except (socket.gaierror, TimeoutError) as e:
    print("There was a problem connecting to the IP, please try again.")
    return 
      
  print(f"Client connected to {HOST} on {PORT}") # Confirm connection

  # SEND THE DATA
  client.sendall(json.dumps({"join": {"username": username, "password": password, "token":""}}).encode()) #Encodes to bytes

  # RECIEVE RESPONSE
  data = client.recv(1024) # Data recieved from server is in bytes

  # GET THE JSON OBJECT AS A DICT
  json_dict = ds_protocol.extract_json(data.decode())

  return json_dict



# Function to facilitate a post to the server
def post(json_dict, client, message):
    try:
      post = {"token": json_dict['response']['token'], "post": {"entry": message, "timestamp": time.time()}}
      client.sendall(json.dumps(post).encode())
      data = client.recv(1024)

      json_dict = json.loads(data.decode())
      
    except (TypeError, json.JSONDecodeError) as e:
      return
    
    return json_dict


# Function to facilitate sending a bio to the server
def bio_post(json_dict, client, bio):
  try:
    bio = {"token": json_dict['response']['token'], "bio": {"entry": bio, "timestamp": ""}}
    client.sendall(json.dumps(bio).encode())
    data = client.recv(1024)

    json_dict = json.loads(data.decode())
    
  except (TypeError, json.JSONDecodeError) as e:
    return
  
  return json_dict


# Will print error if data recieved gives us an errror
def check_errors(response_data: dict):

  if response_data == None:
    print("There was a problem with your request! Try again.")
    return
  
  response = response_data['response']['type']

  if response != 'ok':
    print("Error in DSP protocol -> ", response_data['response']['message'])
  

# Will check if the ip is in correct format
# all it really does is check to see if its only numbers
def valid_ip(ip:str) -> bool:

  ip_list = ip.split('.')
  for e in ip_list:
    try:
      temp = int(e)
      if len(e) > 3 or len(e) == 0:
        return False
      
    except (TypeError, ValueError) as e:
      return False

  return True


              
