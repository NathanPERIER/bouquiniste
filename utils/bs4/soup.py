
from utils.bs4.base import BS4Node
from utils.bs4.tag import Tag
from utils.bs4.exceptions import SelectorNotFoundException

import bs4

from collections.abc import Sequence

class Soup(BS4Node) :

	def __init__(self, soup: "bs4.element.BeautifulSoup", url: str) :
		super().__init__(soup)
		self.url = url
		self.soup = soup
	
	def select(self, selector: str, limit: "int | None" = None) -> "Sequence[Tag]" :
		return [
			Tag(tag, self, f"{selector} #{n}")
			for n, tag in enumerate(self.element.select(selector, limit=limit), start=1)
		]
	
	def select_one(self, selector: str) -> "Tag" :
		res = self.element.select_one(selector)
		if res is None :
			raise SelectorNotFoundException(selector, self)
		return Tag(res, self, selector)

	def getBS4Trace(self) -> str:
		return f"in soup {self.getLongName()} ({self.url})"
	
	
