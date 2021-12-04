from Profile import Profile, Post
from NaClProfile import NaClProfile

path = "/Users/haydenpowers/Documents/UCI/test-folder/journal/bigmama.dsu"

np = NaClProfile()
kp = np.generate_keypair()
print("NP PUBLIC KEY: ", np.public_key)
print("NP PRIVATE KEY: ", np.private_key)
print("NP KEYPAIR: ", np.keypair)

# Test encryption with 3rd party public key
ds_pubkey = "jIqYIh2EDibk84rTp0yJcghTPxMWjtrt5NW4yPZk3Cw="
ee = np.encrypt_entry("Encrypted Message for DS Server", ds_pubkey)

print("EE (ENCRYPTED ENTRY IN TEST): ", ee)

# Add a post to the profile and check that it is decrypted.
np.add_post(Post("Hello Salted World!"))



p_list = np.get_posts()
#print("FROM TEST - GET_ENTRY: ",p_list[0].get_entry())
#print(p_list[0])

# Save the profile
np.save_profile(path)


print("\n\nOpen DSU file to check if message is encrypted.")
input("Press Enter to Continue")

# Create a new NaClProfile object and load the dsu file.
np2 = NaClProfile()
np2.load_profile(path)
# Import the keys
np2.import_keypair(kp)

# Verify the post decrypts properly
p_list = np2.get_posts()
print(type(p_list))
print(p_list[0].get_entry())
#print("ENCRYPTED ENTRY FROM TEST: ", p_list[0].get_entry())
#print("DECRYPTED ENTRY FROM TEST: ", np2._decrypt(p_list[0].get_entry()))