
from utils.bs4 import Soup

import requests
from bs4 import BeautifulSoup

def requestSoup(url: str) -> Soup :
	resp = requests.get(url)
	soup = BeautifulSoup(resp.content, 'html.parser')
	return Soup(soup, url)
