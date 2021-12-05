from NaClProfile import NaClProfile, Post
import json
from pathlib import Path
import ds_client
import input_processor

# path: /Users/haydenpowers/Documents/UCI/test-folder/journal/ajournal.dsu

def main():
    
    PATH = r"C:\Users\hayde\Desktop\College Stuff\UCI\ICS 32\journal\ajournal2.dsu"
    HOST = "168.235.86.101"
    PORT = 3021

    username = "omwtfyb"
    password = "1234"
    bio = "hi"

    profile = NaClProfile()
    profile.generate_keypair()

    profile.load_profile(PATH)

    print("PROFILE TEST - BEFORE POSTS")
    print(type(profile))

    print("PUBLIC KEY: ", profile.public_key)
    print("PRIVATE KEY: ", profile.private_key)
    print("KEYPAIR: ", profile.keypair)
    print("DSU SERVER: ", profile.dsuserver)
    print("USERNAME: ", profile.username)
    print("PASSWORD: ", profile.password)
    print("BIO: ", profile.bio)


    post = Post("this is a post")
    profile.add_post(post)

    post2 = Post("this is a second post")
    profile.add_post(post2)

    posts = profile.get_posts()
    print("\nPOSTS: ", posts)
    #profile.save_profile(PATH)

    print("\nPROFILE TEST - AFTER POSTS")
    profile.load_profile(PATH)

    print("PUBLIC KEY: ", profile.public_key)
    print("PRIVATE KEY: ", profile.private_key)
    print("KEYPAIR: ", profile.keypair)
    print("DSU SERVER: ", profile.dsuserver)
    print("USERNAME: ", profile.username)
    print("PASSWORD: ", profile.password)
    print("BIO: ", profile.bio)

    posts = profile.get_posts()
    print("\nPOSTS: ", posts)
    
    
    
    #pub_k = profile.public_key
    #post = "hola bueno"
    #encrypted_post = profile.encrypt_entry(post, pub_k)

    #ds_client.send(HOST, PORT, username, password, encrypted_post, public_key=pub_k)
    

    #ds_client.send()

    #profile = NaClProfile()
    #ds_client.send(HOST, PORT,
    #            username=username,
    #            password=password,
    #            message=encrypted_post,
    #            bio='')


    


main()
