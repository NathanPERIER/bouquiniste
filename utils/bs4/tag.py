
from utils.bs4.base import BS4Node
from utils.bs4.exceptions import SelectorNotFoundException

import bs4

from typing import Sequence, Collection, MutableSequence

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
		return extractText(self.tag)
	
	def getBS4Trace(self) -> str:
		return f"in tag {self.getLongName()} ({self.query})\n{self.parent.getBS4Trace()}"


def extractText(elements: "Collection[bs4.element.PageElement]") -> str :
	res: "MutableSequence[str]" = []
	for elt in elements :
		if isinstance(elt, bs4.element.NavigableString) :
			if not isinstance(elt, bs4.element.PreformattedString) :
				res.append(str(elt))
		elif isinstance(elt, bs4.element.Tag) :
			if elt.name == 'br' :
				res.append('\n')
			else :
				res.append(extractText(elt))
	return "".join(res).strip()
