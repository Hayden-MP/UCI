# ExtraCreditAPI.py

# Hayden Powers
# powersh@uci.edu
# 56169764

from WebAPI import WebAPI

'''
For extra credit, I decided to use a News API that will get the latest top 3 news headlines on a given topic
    - To use this class, simply instance a ExtraCreditAPI object with the keyword you would like to search for
        By default, this keyword is 'dogs'
    - API key is hardcoded as a global variable
    - Class is inhertied from WebAPI and uses it's _download_url method to get the JSON object
    - 
'''

EXTRACREDITAPIKEY = 'f6b507f4ef2f47779f641d690fc7d8e4'

class ExtraCreditAPI(WebAPI):
    global EXTRACREDITAPIKEY

    def __init__(self, apikey = EXTRACREDITAPIKEY, keyword = 'dogs'):
        super().__init__(apikey=apikey)
        self.keyword = keyword
        self.url = f'https://newsapi.org/v2/everything?q={self.keyword}&apiKey={self.apikey}'
        self.headline_links = None

    # Calls _download_url from WebAPI to get the json object
    def load_data(self):
        r_obj = WebAPI._download_url(self, url=self.url)
        headline_links = {}

        # Get only the top three stories and put them in a dictionary
        for i in range(3):
            headline_links[r_obj['articles'][i]['title']] = r_obj['articles'][i]['url']
       
        self.headline_links = headline_links


    # To add the top three news stories by keyword
    def transclude(self, message:str) -> str:
        if '@extracredit' in message:
            ExtraCreditAPI.load_data(self)

            insertion = '\n\n'
            for i in self.headline_links:
                insertion = insertion + i + "\nLink: " + self.headline_links[i] + "\n\n"
        
            message = message.replace('@extracredit', f"\nTop 3 news stories for {self.keyword}: " + insertion)
        
        return message

'''
def main():
    news_obj = ExtraCreditAPI(keyword='dogs')
    news_obj.load_data()
    news_obj.transclude(message="I like dogs, lets search @extracredit")

main()
'''