import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('odds_api_key')

def get_odds():
    url = f"https://api.the-odds-api.com/v4/sports/mma_mixed_martial_arts/odds?regions=us&markets=h2h&oddsFormat=american&apiKey={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None