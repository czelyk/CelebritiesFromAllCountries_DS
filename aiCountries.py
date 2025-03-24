import requests
import os
from dotenv import load_dotenv
import ollama
import re

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
CX = os.getenv("GOOGLE_CX")

# Initialize the AI Countries class
class AICountries:
    def __init__(self):
        self.model = ollama

    def get_random_countries(self):
        try:
            prompt = "Generate the name of 10 random countries, one celebrity from each, and the country’s ISO 2-letter code. Format: 'Celebrity: <name> - Country Code: <XX>'"
            response = self.model.chat(model="llama2", messages=[{"role": "user", "content": prompt}])
            content = response['message']['content'] if 'message' in response and 'content' in response['message'] else ''
            countries = content.split("\n") if content else ["No countries generated"]
            return [country.strip() for country in countries if country.strip()]
        except Exception as e:
            print(f"Error: {e}")
            return ["Error retrieving countries"]

# Initialize AI Countries
ai_countries = AICountries()