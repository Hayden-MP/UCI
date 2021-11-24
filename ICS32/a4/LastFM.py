# lastfm.py

# Starter code for assignment 4 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Hayden Powers
# powersh@uci.edu
# 56169764

# API key: 79283ba46a968f8b769e2a0ea296a94a
# URL : http://www.last.fm/api/auth/?api_key=xxx


import urllib, json
from urllib import request, error
from WebAPI import WebAPI

'''
This module will return the top 5 tracks from a given musical artist
'''
class LastFM(WebAPI):

    # Object constructor - my default api key and artist Cher
    def __init__(self, apikey='79283ba46a968f8b769e2a0ea296a94a', artist='Cher'):
        super().__init__(apikey=apikey)
        self.artist = artist 
        self.artist_url = artist.replace(' ', '') # Strip whitespace for URL insert
        self.url = f"http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist={self.artist_url}&api_key={self.apikey}&format=json"


    # A method to change the default artist
    def set_artist(self, artist:str) -> None:
        self.artist = artist
        self.artist_url = artist.replace(' ', '')
        LastFM.update_url(self)


    # A method to change the default API
    #def set_apikey(self, apikey:str) -> None:
    #    WebAPI.set_apikey(self, apikey=apikey)
    #    LastFM.update_url(self)


    # This is a helper method that updates the url when the apikey or artist name changes
    def update_url(self):
        self.url = f"http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist={self.artist_url}&api_key={self.apikey}&format=json"
        

    # Calls the web api using the required values and stores the response in class data attributes.
    def load_data(self) -> None:
        top_tracks = []
        r_obj = WebAPI._download_url(self, url=self.url)
        self.artist = r_obj['toptracks']['track'][0]['artist']['name'] # Gets proper punctuation from lastfm
 
        for i in range(5):
            try:
                top_tracks.append(r_obj['toptracks']['track'][i]['name'])
            except KeyError as e:
                print(f"\nInvalid artist name: '{self.artist}'  -- Please check your spelling!")
                break
        
        self.top_tracks = top_tracks
        print(self.top_tracks)


    # For transcluding any message with the @lastfm keyword
    def transclude(self, message:str) -> str:
        if '@lastfm' in message:
            LastFM.load_data(self)

            insertion = ''
            for i in self.top_tracks:
                insertion = insertion + i + ', '

            message = message.replace('@lastfm', f"Top 5 tracks from {self.artist}: " + insertion)
        
        return message

'''
# Main method
def main() -> None:
    lastfm = LastFM(artist='Madonna')
    obj = lastfm.load_data()
    lastfm.set_artist("Cher")
    obj = lastfm.load_data()
    lastfm.set_artist("three doors down")
    obj = lastfm.load_data()

if __name__ == '__main__':
    print()
    main()
    print()
'''