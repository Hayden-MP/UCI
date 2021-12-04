from NaClProfile import NaClProfile, Post
import json
from pathlib import Path
import ds_client
import input_processor

# path: /Users/haydenpowers/Documents/UCI/test-folder/journal/ajournal.dsu

def main():
    '''
    PATH = "/Users/haydenpowers/Documents/UCI/test-folder/journal/bigmama.dsu"
    HOST = "168.235.86.101"
    PORT = 3021

    username = "omwtfyb"
    password = "1234"
    bio = "hi"

    profile = NaClProfile()
    profile.generate_keypair()
    pub_k = profile.public_key
    post = "hola bueno"
    encrypted_post = profile.encrypt_entry(post, pub_k)

    ds_client.send(HOST, PORT, username, password, encrypted_post, public_key=pub_k)
    '''

    ds_client.send()

    #profile = NaClProfile()
    #ds_client.send(HOST, PORT,
    #            username=username,
    #            password=password,
    #            message=encrypted_post,
    #            bio='')


    


main()
