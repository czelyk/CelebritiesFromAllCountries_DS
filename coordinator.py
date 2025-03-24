import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

def get_coordinates(city_name):
    """Fetches the latitude and longitude for a city using Google Geocoding API."""
    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": city_name,
        "key": API_KEY
    }

    response = requests.get(geocode_url, params=params)
    data = response.json()

    if data["status"] == "OK":
        # Get the latitude and longitude from the response
        location = data["results"][0]["geometry"]["location"]
        latitude = location["lat"]
        longitude = location["lng"]
        return latitude, longitude
    else:
        print(f"Could not get coordinates for {city_name}.")
        return None

if __name__ == "__main__":
    # Example usage
    city = "Bursa"  # Replace with your desired city
    coordinates = get_coordinates(city)
    if coordinates:
        print(f"Coordinates for {city}: {coordinates[0]}, {coordinates[1]}")
