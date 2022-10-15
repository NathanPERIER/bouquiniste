
from core.models import ReleaseEntry, PublicationStatus
from utils.bs4 import Soup
from utils.requests import requestSoup

import re
import logging
from typing import Mapping, Tuple

ISBN_FIELD = 'Code EAN'
ILLUSTRATION_FIELD = 'Illustration'
SCENARIO_FIELD = 'Scénario :'
DRAWING_FIELD = 'Dessin :'

illustration_reg = re.compile(r'(\d+) pages?.*')
number_block_reg = re.compile(r'([A-Z]+):\s*(\d+)\s*\(([^)]+)\)\s*')

status_translation = {
	'En cours': PublicationStatus.ONGOING,
	'Terminé': PublicationStatus.FINISHED
}

logger = logging.getLogger(__name__)


def findDetails(entry: ReleaseEntry) :
	soup = requestSoup(entry.link)
	price = soup.select('div#prixnumber', 1)
	if len(price) > 0 :
		entry.price = price[0].innerText()
	readNumberBlock(entry, soup)
	readTopInfo(entry, soup)
	

def readNumberBlock(entry: ReleaseEntry, soup: Soup) :
	number_block = soup.select_one('div#numberblock')
	matches: "Mapping[str,Tuple[int,PublicationStatus]]" = {}
	for m in number_block_reg.findall(number_block.innerText()) :
		if m[2] in status_translation :
			status = status_translation[m[2]]
		else :
			status = PublicationStatus.UNKNOWN
			logger.info("No translation found for status %s", m[2])
		matches[m[0]] = (int(m[1]), status)
	if 'VF' in matches :
		entry.status = matches['VF'][1]
	if 'VO' in matches :
		entry.pub_number, entry.pub_status = matches['VO']


def readTopInfo(entry: ReleaseEntry, soup: Soup) :
	top_info: "Mapping[str,str]" = {}
	for elt in soup.select('div#topinfo > ul > li') :
		line = elt.innerText().split(':', 1)
		top_info[line[0].strip()] = line[1].strip()
	if ISBN_FIELD in top_info :
		entry.isbn = top_info[ISBN_FIELD]
	if ILLUSTRATION_FIELD in top_info :
		match = illustration_reg.fullmatch(top_info[ILLUSTRATION_FIELD])
		if match is not None :
			entry.pages = int(match.group(1))
			if entry.pages <= 0 :
				entry.pages = None
	if SCENARIO_FIELD in top_info :
		entry.author = top_info[SCENARIO_FIELD]
	elif DRAWING_FIELD in top_info :
		entry.author = top_info[DRAWING_FIELD]
	


