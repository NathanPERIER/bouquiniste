
from core.models import ReleaseEntry

from typing import Sequence

from datetime import date


class Source :

	def getEntries(self, begin: date, end: date) -> "Sequence[ReleaseEntry]" :
		raise NotImplementedError()

	def refineEntry(self, entry: ReleaseEntry) :
		raise NotImplementedError()
