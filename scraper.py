import os
import requests
import logging
import re
from dotenv import load_dotenv
from aiCountries import AICountries
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
CX = os.getenv("GOOGLE_CX")

# Validate API keys
if not API_KEY or not CX:
    logging.error("Missing API credentials. Please check your .env file.")
    exit(1)

# Initialize the AI Countries class
ai_countries = AICountries()

# Create the 'pictures' folder if it doesn't exist
PICTURES_FOLDER = os.path.join(os.getcwd(), "pictures")
os.makedirs(PICTURES_FOLDER, exist_ok=True)

def fetch_image_url(query: str) -> Optional[str]:
    """Fetches the first image URL from Google Custom Search API."""
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": f"{query} portrait",
        "cx": CX,
        "key": API_KEY,
        "searchType": "image",
        "num": 1
    }
    try:
        response = requests.get(search_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("items", [{}])[0].get("link")
    except requests.RequestException as e:
        logging.error(f"Failed to fetch image for {query}: {e}")
    except KeyError:
        logging.warning(f"Unexpected response format for {query}.")
    return None

def download_image(image_url: str, country_code: str) -> None:
    """Downloads an image from the given URL and saves it."""
    try:
        img_data = requests.get(image_url, timeout=5).content
        file_path = os.path.join(PICTURES_FOLDER, f"{country_code.lower()}.jpg")
        with open(file_path, 'wb') as f:
            f.write(img_data)
        logging.info(f"Image saved as {file_path}")
    except requests.RequestException as e:
        logging.error(f"Error downloading image for {country_code}: {e}")
    except IOError as e:
        logging.error(f"File error: {e}")

def process_entries(entries: list[str]) -> None:
    """Processes each entry, extracts celebrity name and country code, and downloads images."""
    for entry in entries:
        logging.debug(f"Processing entry: {entry}")
        match = re.search(r"Celebrity: (.+?) - Country Code: (\w{2})", entry)
        if match:
            celebrity_name, country_code = match.groups()
            logging.info(f"Fetching image for {celebrity_name} from {country_code.upper()}")
            image_url = fetch_image_url(celebrity_name)
            if image_url:
                download_image(image_url, country_code)
            else:
                logging.warning(f"No image found for {celebrity_name}.")
        else:
            logging.warning(f"Skipping invalid entry: {entry}")

if __name__ == "__main__":
    logging.info("Generating random countries and celebrities...")
    random_countries = ai_countries.get_random_countries()
    logging.debug(f"Raw AI Output: {random_countries}")
    process_entries(random_countries)