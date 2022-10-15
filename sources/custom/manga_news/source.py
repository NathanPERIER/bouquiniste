
from sources.base import Source
from core.models import ReleaseEntry
from sources.custom.manga_news.listing import getFirstListingPage, getNextListingPage
from sources.custom.manga_news.details import findDetails
from utils.wrappers import FlattenIterator

from datetime import date
from typing import Iterable, Iterator, Sequence, Tuple


class MangaNewsSource(Source) :

	def getEntries(self, begin: date, end: date) -> "Iterable[ReleaseEntry]" :
		if begin.month == end.month and begin.year == end.year :
			return FlattenIterator(OneMonthIterable(begin.month, begin.year, begin.day, end.day))
		return FlattenIterator(MultiMonthsIterable(begin, end))

	def refineEntry(self, entry: ReleaseEntry) :
		findDetails(entry)



class MultiMonthsIterable(Iterator[Sequence[ReleaseEntry]]) :
	
	def __init__(self, begin: date, end: date) :
		self.begin = begin
		self.end = end
		self.current = begin
		self.page = getFirstListingPage(begin.month, begin.year)
		self.last_month = False
		self.found_one = False
		self.reached_end = False
	
	def nextPage(self) :
		# Try to get the next page for the current month
		page = getNextListingPage(self.page)
		if page is not None :
			self.page = page
			return
		# If we reached the end of the month, try and switch to the next month
		if self.last_month :
			# If we're already in the last month, stop iterating
			# (happens if the last day of the range is the last day of the month)
			raise StopIteration
		self.found_one = True # Forces to leave the state when we probe for the beginning of the range
		self.current = self.current.replace(month = self.current.month + 1)
		if self.current.month == self.end.month and self.current.year == self.end.year :
			self.last_month = True
		self.page = getFirstListingPage(self.current.month, self.current.year)
	
	def __next__(self) -> "Sequence[ReleaseEntry]" :
		if self.reached_end :
			raise StopIteration
		if self.last_month :
			return self.nextNearEnd()
		if self.found_one :
			return self.nextWithinRange()
		return self.nextProbingBeginning()
	
	def nextProbingBeginning(self) -> "Sequence[ReleaseEntry]" :
		res = [
			x for x in self.page.listing
			if x.release >= self.begin
		]
		if len(res) > 0 :
			self.found_one = True
		self.nextPage()
		return res
	
	def nextWithinRange(self) -> "Sequence[ReleaseEntry]" :
		res = self.page.listing
		self.nextPage()
		return res
	
	def nextNearEnd(self) -> "Sequence[ReleaseEntry]" :
		res = [
			x for x in self.page.listing
			if x.release <= self.end
		]
		if len(res) < len(self.page.listing) :
			self.reached_end = True
		else :
			self.nextPage()
		return res
	
	

class OneMonthIterable(Iterator[Sequence[ReleaseEntry]]) :

	def __init__(self, month: int, year: int, begin_day: int, end_day: int) :
		self.month = month
		self.year = year
		self.begin_day = begin_day
		self.end_day = end_day
		self.found_any = False
		self.page = getFirstListingPage(month, year)
	
	def __next__(self) -> "Sequence[ReleaseEntry]" :
		if not self.found_any :
			return self.nextBeforeFind()
		return self.nextAfterFind()
	
	def filterUpperBound(self, seq: "Sequence[ReleaseEntry]") -> "Tuple[bool,Sequence[ReleaseEntry]]" :
		res = [
			x for x in seq
			if x.release.day <= self.end_day
		]
		return len(res) < len(seq), res
	
	def nextBeforeFind(self) -> "Sequence[ReleaseEntry]" :
		if self.page is None :
			raise StopIteration
		filtered = [
			x for x in self.page.listing
			if x.release.day >= self.begin_day
		]
		self.page = getNextListingPage(self.page)
		if len(filtered) > 0 :
			self.found_any = True
			removed, res = self.filterUpperBound(filtered)
			if removed :
				self.page = None
			return res
		return filtered
	
	def nextAfterFind(self) -> "Sequence[ReleaseEntry]" :
		if self.page is None :
			raise StopIteration
		removed, res = self.filterUpperBound(self.page.listing)
		self.page = None if removed else getNextListingPage(self.page)
		return res
