# openweather.py

# Starter code for assignment 4 in ICS 32 Programming with 
# Software Libraries in Python

# Replace the following placeholders with your information.

# Hayden Powers
# powersh@uci.edu
# 56169764

import urllib, json
from urllib import request, error

class OpenWeather:

    # Constructor of OpenWeather class
    def __init__(self, zipcode="92028", ccode="US", apikey='9ccb0ef809ff98bdefababd7b3cc4dc4'):
        self.ccode = ccode
        self.apikey = apikey
        self.zipcode = zipcode
        self.url = f"http://api.openweathermap.org/data/2.5/weather?zip={zipcode},{ccode}&appid={apikey}"
        self.longitude = None
        self.latitude = None
        self.description = None
        self.temperature = None
        self.high_temperature = None
        self.low_temperature = None
        self.feels_like = None
        self.pressure = None
        self.humidity = None
        self.visibility = None
        self.wind_speed = None
        self.wind_degree = None
        self.city = None
        self.sunrise = None
        self.sunset = None


    # Sets the class object's API key given as a parameter
    def set_apikey(self, apikey:str) -> None:
        self.apikey = apikey
        self.url = f"http://api.openweathermap.org/data/2.5/weather?zip={self.zipcode},{self.ccode}&appid={self.apikey}"


    # Calls the web api using the required values and stores the response in class data attributes.
    def load_data(self) -> None:
        response = None
        r_obj = None

        try:
            response = urllib.request.urlopen(self.url)
            json_results = response.read()
            r_obj = json.loads(json_results)

        except urllib.error.HTTPError as e:
            print('Failed to download contents of URL')
            print('Status code: {}'.format(e.code))
            if e.code == 404:
                print("URL not recognized, check your input values")
            elif e.code == 503:
                print("Server is down or unavailable")
            return
        
        except urllib.error.URLError as e:
            print('Network issue, check connection to internet')
            print('Status code: {}'.format(e))
            return

        finally:
            if response != None:
                response.close()

        # Set all the class attributes to API information
        self.longitude = r_obj['coord']['lon']
        self.latitude = r_obj['coord']['lat']
        self.description = r_obj['weather'][0]['description']
        self.temperature = r_obj['main']['temp']
        self.high_temperature = r_obj['main']['temp_max']
        self.low_temperature = r_obj['main']['temp_min']
        self.feels_like = r_obj['main']['feels_like']
        self.pressure = r_obj['main']['pressure']
        self.humidity = r_obj['main']['humidity']
        self.visibility = r_obj['visibility']
        self.wind_speed = r_obj['wind']['speed']
        self.wind_degree = r_obj['wind']['deg']
        self.city = r_obj['name']
        self.sunrise = r_obj['sys']['sunrise']
        self.sunset = r_obj['sys']['sunset']

        return r_obj


    def transclude(self, message:str) -> str:
        '''
        Replaces keywords in a message with associated API data.
        :param message: The message to transclude

        :returns: The transcluded message
        '''
        if '@weather' in message:
            OpenWeather.load_data(self)
            print("KEYWORD CAUGHT")
            message = message.replace('@weather', self.description)
        
        return message


