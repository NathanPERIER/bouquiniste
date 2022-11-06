from core.models import ReleaseEntry
from utils.bs4 import Soup, Tag
from utils.requests import requestSoup
from utils.exceptions import FormatException

import re
from datetime import datetime
from collections.abc import Sequence

BASE_URL = 'https://www.manga-news.com'

title_reg = re.compile(r'(.+?)(?: Vol.([0-9]+))?')


class ListingPage :
	def __init__(self) :
		self.listing: "Sequence[ReleaseEntry]"
		self.prev: "str | None" = None
		self.next: "str | None" = None


def getFirstListingPage(month: int, year: int) -> ListingPage :
	url = f"https://www.manga-news.com/index.php/planning?p_year={year}&p_month={month}"
	soup = requestSoup(url)
	return readListingPage(soup)


def getNextListingPage(page: ListingPage) -> "ListingPage | None" :
	if page.next is None :
		return None
	soup = requestSoup(f"{BASE_URL}{page.next}")
	return readListingPage(soup)


def readListingPage(soup: Soup) -> ListingPage :
	res = ListingPage()
	pager_elts = soup.select('div.pager > span.pagerblock > a')
	if len(pager_elts) == 0 :
		res.listing = []
		return res
	res.listing = [
		readListingItem(item)
		for item in soup.select('#listing-chroniques > .listing-item')
	]
	if pager_elts[0].innerText() == '«' :
		res.prev = pager_elts[0]['href']
	if pager_elts[-1].innerText() == '»' :
		res.next = pager_elts[-1]['href']
	return res


def readListingItem(item: Tag) -> ReleaseEntry :
	res = ReleaseEntry()
	title = item.select_one('a.title')
	res.link = title['href']
	match = title_reg.fullmatch(title.innerText().strip())
	if match is None :
		raise FormatException(f"Title {title} does not match regex {title_reg.pattern}")
	res.title = match.group(1).strip()
	if match.group(2) is not None :
		res.number = int(match.group(2))
	res.editor = item.select_one('span.editor').innerText().strip()
	res.image = item.select_one('img.entryPicture')['src']
	if len(res.image) == 0 :
		res.image = None
	date_text = item.select_one('span.date_out').innerText().strip()
	res.release = datetime.strptime(date_text, 'Sortie le %d/%m/%Y').date()
	return res
