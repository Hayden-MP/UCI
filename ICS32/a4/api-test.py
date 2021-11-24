import urllib, json
from urllib import request, error
from OpenWeather import OpenWeather
from LastFM import LastFM
from ExtraCreditAPI import ExtraCreditAPI
from WebAPI import WebAPI


# Open weather API key : 9ccb0ef809ff98bdefababd7b3cc4dc4

def _download_url(url_to_download: str) -> dict:
    response = None
    r_obj = None

    try:
        response = urllib.request.urlopen(url_to_download)
        json_results = response.read()
        r_obj = json.loads(json_results)

    except urllib.error.HTTPError as e:
        print('Failed to download contents of URL')
        print('Status code: {}'.format(e.code))
    
    finally:
        if response != None:
            response.close()
    
    return r_obj

def process() -> None:
    zip = "92028"
    ccode = "US"
    apikey = "9ccb0ef809ff98bdefababd7b3cc4dc4"
    url = f"http://api.openweathermap.org/data/2.5/weather?zip={zip},{ccode}&appid={apikey}"

    weather_obj = _download_url(url)
    if weather_obj is not None:
        print("Temp: ", weather_obj['main']['temp'])
        print("Feels like: ", weather_obj['main']['feels_like'])
        print("Description: ", weather_obj['weather'][0]['description'])
        print("Wind speed: ", weather_obj['wind']['speed'])
        print("\nComplete object:\n")
        print(weather_obj)


def test_api(message:str, apikey:str, webapi:WebAPI):
    webapi.set_apikey(apikey)
    webapi.load_data()
    result = webapi.transclude(message)
    print(result)



def main():
    #apikey = input("Enter your API key: ")
    #zip = input("Enter your ZIP code: ")
    #ccode = input("Enter your Country code (if from US, type 'US'): ")

    #weather_obj = OpenWeather(zip, ccode, apikey)
    #obj = OpenWeather.load_data(weather_obj)
    #print(obj)
    '''
    zipcode = "92697"
    ccode = "US"
    apikey = "9ccb0ef809ff98bdefababd7b3cc4dc4"

    open_weather = OpenWeather(zipcode, ccode)
    open_weather.set_apikey(apikey)
    open_weather.load_data()

    print(f"The temperature for {zipcode} is {open_weather.temperature} degrees")
    print(f"The high for today in {zipcode} will be {open_weather.high_temperature} degrees")
    print(f"The low for today in {zipcode} will be {open_weather.low_temperature} degrees")
    print(f"The coordinates for {zipcode} are {open_weather.longitude} longitude and {open_weather.latitude} latitude")
    print(f"The current weather for {zipcode} is {open_weather.description}")
    print(f"The current humidity for {zipcode} is {open_weather.humidity}")
    print(f"The sun will set in {open_weather.city} at {open_weather.sunset}")
    '''


    open_weather = OpenWeather() #notice there are no params here...HINT: be sure to use parameter defaults!!!
    lastfm = LastFM()
    extracredit = ExtraCreditAPI()

    test_api("Testing the weather: @weather", '9ccb0ef809ff98bdefababd7b3cc4dc4', open_weather)
    # expected output should include the original message transcluded with the default weather value for the @weather keyword.

    test_api("Testing lastFM: @lastfm", '79283ba46a968f8b769e2a0ea296a94a', lastfm)
    # expected output include the original message transcluded with the default music data assigned to the @lastfm keyword

    test_api("Testing ExtraCreditAPI: @extracredit", 'f6b507f4ef2f47779f641d690fc7d8e4', extracredit)
    # expected output include the original message transcluded with the default music data assigned to the @lastfm keyword



if __name__ == '__main__':
    print()
    main()
    print()

'''
NOTES:
- Ask TA about my exception handling to see if it is sufficient
- Ask about how to test "invalid dta formatting from the remote API"
- Ask TA how to read responses from API when we just get 
    <http.client.HTTPResponse object at 0x105485430> and .read() gives us
    a whole XML (in lastfm)
'''
