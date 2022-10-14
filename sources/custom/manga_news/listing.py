from core.models import ListItem
from utils.bs4 import Soup, Tag

import re
from datetime import datetime
from collections.abc import Sequence

title_reg = re.compile(r'(.+?)(?: Vol.([0-9]+))?')


class ListingPage :
	def __init__(self) :
		self.listing: "Sequence[ListItem]"
		self.prev: "str | None" = None
		self.next: "str | None" = None


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


def readListingItem(item: Tag) -> ListItem :
	res = ListItem()
	title = item.select_one('a.title')
	res.link = title['href']
	match = title_reg.fullmatch(title.innerText().strip())
	if match is None :
		# TODO new exception type
		raise Exception(f"Title {title} does not match regex {title_reg.pattern}")
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
