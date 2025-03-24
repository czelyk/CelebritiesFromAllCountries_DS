import requests

class GoogleImageSearch:
    def __init__(self, api_key, cx):
        self.api_key = api_key
        self.cx = cx
        self.search_url = "https://www.googleapis.com/customsearch/v1"

    def get_image_url(self, query):
        params = {
            "q": query,
            "cx": self.cx,
            "key": self.api_key,
            "searchType": "image",
            "num": 1
        }
        response = requests.get(self.search_url, params=params)
        data = response.json()

        if "items" in data:
            return data["items"][0]["link"]
        else:
            return None
