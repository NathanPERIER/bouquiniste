
from core.models import ReleaseEntry

from typing import Iterable, MutableSequence, Optional

from datetime import date

__all__ = [
	"Source", 
	"SourceInfo"
]


class SourceInfo :
	def __init__(self, name: str) :
		self.name = name
		self.image: "str | None" = None
		self.accepted_urls: "MutableSequence[str]" = []
	
	def addPattern(self, pattern: str) :
		self.accepted_urls.append(pattern)


class Source :

	def __init__(self, info: SourceInfo) :
		self.info = info

	def getEntries(self, begin: date, end: date) -> "Iterable[ReleaseEntry]" :
		raise NotImplementedError()

	def refineEntry(self, entry: ReleaseEntry) :
		raise NotImplementedError()
	
	def getInfo(self) -> SourceInfo :
		return self.info
	
