# lastfm.py

# Starter code for assignment 4 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Hayden Powers
# powersh@uci.edu
# 56169764

# API key: 79283ba46a968f8b769e2a0ea296a94a
# URL : http://www.last.fm/api/auth/?api_key=xxx


#class LastFM:

#    def __init__(self, ):


import urllib, json
from urllib import request, error
import xml.dom.minidom


def _download_url(url_to_download: str) -> dict:
    response = None
    r_obj = None

    try:
        response = urllib.request.urlopen(url_to_download)
        print("\RESPONSE: ", response, "\n\n")
        results = response.read()
        #print("\nRESULTS: ", results, "\n\n")
        r_obj = json.loads(results)
        print(r_obj['track']['name'])

    except urllib.error.HTTPError as e:
        print('Failed to download contents of URL')
        print('Status code: {}'.format(e.code))
    
    finally:
        if response != None:
            response.close()
    
    return r_obj

# For Part 2 
def transclude(self, message:str) -> str:
  '''
  Replaces keywords in a message with associated API data.
  :param message: The message to transclude
	
  :returns: The transcluded message
  '''
  #TODO: write code necessary to transclude keywords in the message parameter with appropriate data from API
  pass


# Main method
def main() -> None:
    apikey = "79283ba46a968f8b769e2a0ea296a94a"
    #url = "http://www.last.fm/api/auth/?api_key={}&format=json".format(apikey)
    url = f"https://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={apikey}&artist=cher&track=believe&format=json"
    obj = _download_url(url)
    if obj is not None:
        print(obj['track']['name'])


if __name__ == '__main__':
    print()
    main()
    print()