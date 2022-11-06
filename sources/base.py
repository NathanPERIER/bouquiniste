
from core.models import ReleaseEntry, SourceInfo

from typing import Iterable

from datetime import date


class Source :

	def getEntries(self, begin: date, end: date) -> "Iterable[ReleaseEntry]" :
		raise NotImplementedError()

	def refineEntry(self, entry: ReleaseEntry) :
		raise NotImplementedError()
	
	def getInfo(self) -> SourceInfo :
		raise NotImplementedError()
