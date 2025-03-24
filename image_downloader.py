import requests

class ImageDownloader:
    def __init__(self, image_url):
        self.image_url = image_url

    def download(self):
        if not self.image_url:
            print("No image URL provided.")
            return None
        print("Downloading image from:", self.image_url)
        img_data = requests.get(self.image_url).content
        return img_data
