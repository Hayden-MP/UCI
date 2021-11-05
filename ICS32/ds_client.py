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

# a3 calls this send method after collecting info
# We should gather certain info in different methods?

def send(server:str, port:int, username:str, password:str, message:str, bio:str=None):
  '''
  The send function joins a ds server and sends a message, bio, or both

  :param server: The ip address for the ICS 32 DS server.
  :param port: The port where the ICS 32 DS server is accepting connections.
  :param username: The user name to be assigned to the message.
  :param password: The password associated with the username.
  :param message: The message to be sent to the server.
  :param bio: Optional, a bio for the user.
  '''

  HOST = server
  PORT = port

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:

    json_dict = join(HOST, PORT, client, username, password)
    print("JSON_DICT from DS_CLIENT: ", json_dict)

    post_response = post(json_dict, client, message)
    print("POST_RESPONSE from DS_CLIENT: ", post_response)

    if bio != None:
      bio_response = bio_post(json_dict, client, bio)
      print("BIO_RESPONSE from DS_CLIENT: ", bio_response)


# Function to facilitate joining the server
def join(HOST, PORT, client, username, password):
  
  # Connect to our server here
  client.connect((HOST, PORT))
  print(f"Client connected to {HOST} on {PORT}") # Confirm connection

  # SEND THE DATA
  client.sendall(json.dumps({"join": {"username": username, "password": password, "token":""}}).encode()) #Encodes to bytes

  # RECIEVE RESPONSE
  data = client.recv(1024) # Data recieved from server is in bytes

  # PRINT DECODED DATA (STRING)
  print(data.decode())

  # GET THE JSON OBJECT AS A DICT
  json_dict = ds_protocol.extract_json(data.decode())

  return json_dict



# SHOULD THESE BE IN DS_PROTOCOL?? VVV

# Function to facilitate a post to the server
def post(json_dict, client, message):
    post = {"token": json_dict['response']['token'], "post": {"entry": message, "timestamp": time.time()}}
    client.sendall(json.dumps(post).encode())
    data = client.recv(1024)
    return data.decode()


# Function to facilitate sending a bio to the server
def bio_post(json_dict, client, bio):
    bio = {"token": json_dict['response']['token'], "bio": {"entry": bio, "timestamp": ""}}
    client.sendall(json.dumps(bio).encode())
    data = client.recv(1024)
    return data.decode()


# This will handle any error that is returned from the join, post, or bio commands
def handle_errors(json_dict):
  response = json_dict['response']['type']

  if response == 'error':
    print("ERROR CAUGHT")



              
