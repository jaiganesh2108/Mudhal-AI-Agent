import requests
from bs4 import BeautifulSoup
import pandas as pd

def connect_website(url):
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error connecting to website: {e}")
        return None