# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Hayden Powers
# powersh@uci.edu
# 56169764

#  This is the distributed social client module. It contains all code required
#  to exchange messages with the DSP Server

'''
NOTES:
- To connect to the server, in our join function we need: username, password, and public key
- We recieve a response from the server and the server public key
- We then encrypt the post with the SERVER public key and OUR private key
- We then send the post with our pubilc key
'''

import socket
import ds_protocol
import json
import time
from NaClProfile import NaClProfile


# Send function sends the dsu file information to the DSP server
def send(username:str="ItsJeffBezos", password:str="amazon", message:str="i am richer than you", bio:str="This is Bezos, betch", public_key:str=''):

  HOST = "168.235.86.101"
  PORT = 3021
  profile = NaClProfile()
  profile.generate_keypair()
  public_key = profile.public_key
  
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:

    json_dict = join(HOST, PORT, client, username, password, public_key)
    server_key = json_dict['response']['token']
    check_errors(json_dict)

    # ENCRYPT THE MESSAGE USING SERVER KEY
    encrypted_msg = profile.encrypt_entry(message, server_key)

    post_response = post(json_dict, client, encrypted_msg, public_key) 
    check_errors(post_response)

    if bio != None: 
      # ENCRYPT BIO
      encryped_bio = profile.encrypt_entry(bio, server_key)
      bio_response = bio_post(json_dict, client, encryped_bio, public_key) # *******
      check_errors(bio_response)


# Function to facilitate joining the server
def join(HOST, PORT, client, username, password, public_key):
  # Connect to our server here
  try:
    client.connect((HOST, PORT))
    
  except (socket.gaierror, TimeoutError) as e:
    print("There was a problem connecting to the IP, please try again.")
    return 
      
  print(f"Client connected to {HOST} on {PORT}") # Confirm connection

  # SEND THE DATA
  client.sendall(json.dumps({"join": {"username": username, "password": password, "token": public_key}}).encode()) #Encodes to bytes

  # RECIEVE RESPONSE
  data = client.recv(1024) # Data recieved from server is in bytes
  json_dict = ds_protocol.extract_json(data.decode()) # GET THE JSON OBJECT AS A DICT

  return json_dict



# Function to facilitate a post to the server
def post(json_dict, client, message, public_key):
    try:
      post = {"token": public_key, "post": {"entry": message, "timestamp": time.time()}}      
      client.sendall(json.dumps(post).encode())
      data = client.recv(1024)

      json_dict = json.loads(data.decode())
      
    except (TypeError, json.JSONDecodeError) as e:
      return
    
    return json_dict


# Function to facilitate sending a bio to the server
def bio_post(json_dict, client, encrypted_bio, public_key):
  try:
    bio = {"token": public_key, "bio": {"entry": encrypted_bio, "timestamp": ""}}
    client.sendall(json.dumps(encrypted_bio).encode())
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


              
