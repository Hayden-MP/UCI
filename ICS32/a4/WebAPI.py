# webapi.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Hayden Powers
# powersh@uci.edu
# 56169764

from abc import ABC, abstractmethod
from urllib import request, error
import urllib, json

class WebAPI(ABC):

  def __init__(self, apikey=''):
    self.apikey = apikey 
    
  # Base class methods needed for all our API's
  def _download_url(self, url: str) -> dict:
    response = None
    r_obj = None

    try:
      response = urllib.request.urlopen(url)
      results = response.read()
      r_obj = json.loads(results)

    except urllib.error.HTTPError as e:
      print('Failed to download contents of URL')
      print('Status code: {}'.format(e.code))
    
    finally:
        if response != None:
                response.close()

    return r_obj
	
  # A method that will set the api key for the class
  def set_apikey(self, apikey:str) -> None:
    self.apikey = apikey
	
  # Our derived API classes will need to implement these abstract methods
  @abstractmethod
  def load_data(self):
    pass
  
  @abstractmethod
  def transclude(self, message:str) -> str:
    pass
