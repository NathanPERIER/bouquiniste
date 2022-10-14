
from utils.bs4.base import BS4Node
from utils.bs4.exceptions import SelectorNotFoundException

import bs4

from collections.abc import Sequence

class Tag(BS4Node) :

	def __init__(self, tag: bs4.element.Tag, parent: BS4Node, query: str) -> None:
		super().__init__(tag)
		self.tag = tag
		self.parent = parent
		self.query = query
	
	def select(self, selector: str, limit: "int | None" = None) -> "Sequence[Tag]" :
		return [
			Tag(tag, self, f"{selector} #{n}")
			for n, tag in enumerate(self.tag.select(selector, limit=limit), start=1)
		]
	
	def select_one(self, selector: str) -> "Tag" :
		res = self.tag.select_one(selector)
		if res is None :
			raise SelectorNotFoundException(selector, self)
		return Tag(res, self, selector)
	
	def innerText(self) -> str :
		# TODO can do better...
		return self.tag.text
	
	def getBS4Trace(self) -> str:
		return f"in tag {self.getLongName()} ({self.query})\n{self.parent.getBS4Trace()}"
