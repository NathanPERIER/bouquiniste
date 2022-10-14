
import bs4

from collections.abc import Sequence

class BS4Node :

	def __init__(self, element: "bs4.element.BeautifulSoup | bs4.element.Tag") :
		self.element = element

	def getName(self) -> str :
		return self.element.name
	
	def getLongName(self) -> str :
		res = self.element.name
		classes = self['class']
		identifier = self['id']
		if len(classes) > 0 :
			res += "." + classes.replace(' ', '.')
		if len(identifier) > 0 :
			return f"{res}#{identifier}"
		return res
	
	def getBS4Trace(self) -> str :
		raise NotImplementedError()

	def __getitem__(self, name: str) -> str :
		res = self.element[name]
		if isinstance(res, list) :
			return " ".join(res)
		return res