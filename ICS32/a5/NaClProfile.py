# NaClProfile.py
# An encrypted version of the Profile class provided by the Profile.py module
# 
# for ICS 32
# by Mark S. Baldwin

'''
QUESTIONS:
- What is a nonce?
- I generated the keys in the initializer function, what is the purpose of 
    the generate_key function? Wouldnt it just generate a whole new set of keys?
- NaCl examples https://pynacl.readthedocs.io/en/latest/public/#examples
- Have to convert a string message to bytes in order to encrypt the message
- message = "hello" .. encoded_message = message.encode(encoding='UTF-8')
- encoding turns string into bytes, encrypting turns bytes into encrypted bytes
- encrypted_message = boxed_keys.encrypt(plaintext encoded_message, encoder=encoding.Base64Encoder)
- In order to send to the server, we need to decode the encrypted message (post/bio) to turn it 
    back into a string
- show(encrypted_message.decode(encoding='UTF-8')) -> prints as string 
- To decrypt, use the box again to decrypt decrypted_message = boxed_keys.decrypt(encrypted msg, encoder=..)
- decoded_message = decrypted_message.decode(encoding='UTF-8'..)
- show(decoded_message)
- Crypto error may be a result of trying to decrypt different keys that were sent back from server
'''
from nacl import public, encoding
import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box
from Profile import Profile, Post
from NaClDSEncoder import NaClDSEncoder
import json, os
from pathlib import Path
import copy
    
class NaClProfile(Profile):
    # NaClProfile constructor
    def __init__(self, dsuserver = None, keypair = None, username='d_username', password='d_password', bio='d_bio'):
        self.public_key = ''
        self.private_key = ''
        self.keypair = ''
        self.username = username
        self.password = password
        self.bio = bio
        
        if keypair != None:
            self.import_keypair(keypair)
        
        super().__init__(dsuserver)

    # Private encryption method to use within the class
    def _encrypt(self, private_key, public_key, message:str) -> str:
        # STEP 1 - USE NACLDSENCODER TO CONVERT KEYS INTO NACL PRIVATEKEY() and PUBLICKEY()
        nacl_en = NaClDSEncoder()
        priv_k = nacl_en.encode_private_key(private_key=private_key)
        pub_k = nacl_en.encode_public_key(public_key=public_key)

        # STEP 2 - ENCODE THE MESSAGE TO BYTES
        encoded_msg = message.encode(encoding="UTF-8")
        
        # STEP 3 - ENCRYPT THE MESSAGE USING BOX, PASSING IN PRIVATEKEY() AND PUBLICKEY() from STEP 1
        box = Box(private_key=priv_k, public_key=pub_k)
        encrypted_msg = box.encrypt(encoded_msg, encoder=encoding.Base64Encoder)

        # STEP 4 - CONVERT ENCRYPTED MESSAGE BACK TO STRING
        encrypted_string = encrypted_msg.decode(encoding='UTF-8')
        
        return encrypted_string


    # Private decryption method to use within the class
    def _decrypt(self, private_key, public_key, encrypted_msg):
        # STEP 1 - USE NACLDSENCODER TO CONVERT KEYS INTO NACL PRIVATEKEY() and PUBLICKEY()
        nacl_en = NaClDSEncoder()
        priv_k = nacl_en.encode_private_key(private_key=private_key)
        pub_k = nacl_en.encode_public_key(public_key=public_key)
        
        # STEP 2 MAKE A BOX WITH THE KEYS AND DECRYPT MESSAGE
        box = Box(priv_k, pub_k)
        decrypted_msg = box.decrypt(ciphertext=encrypted_msg, encoder=encoding.Base64Encoder)

        # STEP 3 RETURN DECODED AND DECRYPTED MESSAGE
        decoded_msg = decrypted_msg.decode('UTF-8')
        return decoded_msg


    # This method uses the NaClDSEncoder module to generate a new keypair and populate
    # the public data attributes created in the initializer
    def generate_keypair(self) -> str:
        nacl_enc = NaClDSEncoder()
        nacl_enc.generate() # Generate keys
        self.public_key = nacl_enc.public_key
        self.private_key = nacl_enc.private_key
        self.keypair = nacl_enc.keypair
        return self.keypair


    # This method imports an existing keypair parameter to populate the 
    # public data attributes created by the initializer.
    def import_keypair(self, keypair: str):
        self.keypair = keypair
        self.public_key = keypair[:44]
        self.private_key = keypair[44:]


    # Override the add_post method to encrypt post entries as they are added.
    def add_post(self, post: Post) -> None:
        # Get the post entry and use _encrypt method
        post_entry = post.get_entry()
        encrypted_entry = self._encrypt(self.private_key, self.public_key, post_entry)
        post.set_entry(encrypted_entry) 
        super().add_post(post)
        

    # Override the get_posts method to decrypt post entries.
    def get_posts(self) -> list:
        posts = copy.deepcopy(super().get_posts())

        # Go through all the encrypted posts and decrypt/decode them, 
        # assign each to entry and return posts
        for post in posts:
            post.set_entry(self._decrypt(self.private_key, self.public_key, post.get_entry()))

        return posts
    

    def load_profile(self, path: str) -> None:
        p = Path(path)

        print("\nLOAD_PROFILE CALLED FROM NACLPROFILE\n")

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)

                print("JSON OBJ FROM NACLPROFIILE: ", obj)

                self.public_key = obj['public_key']
                self.private_key = obj['private_key']
                self.keypair = obj['keypair']
                self.dsuserver = obj['dsuserver']
                self.username = obj['username']
                self.password = obj['password']
                self.bio = obj['bio']
                
                for post_obj in obj['_posts']:
                    post = Post(post_obj['entry'], post_obj['timestamp'])
                    self._posts.append(post)
                f.close()

            except Exception as ex:
                raise Profile.DsuProfileError(ex)
        else:
            raise Profile.DsuFileError()


    def encrypt_entry(self, entry:str, public_key:str) -> bytes:
        return self._encrypt(self.private_key, public_key, entry)

        # Is this all I have to do here?

