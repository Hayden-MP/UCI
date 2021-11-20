# webapi.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Hayden Powers
# powersh@uci.edu
# 56169764

from abc import ABC, abstractmethod

class WebAPI(ABC):

  # ALL status code error handling goes here 
  
  def _download_url(self, url: str) -> dict:
    #TODO: Implement web api request code in a way that supports ALL types of web APIs
    pass
	
  def set_apikey(self, apikey:str) -> None:
    pass
	
  @abstractmethod
  def load_data(self):
    pass
	
  @abstractmethod
  def transclude(self, message:str) -> str:
    pass
