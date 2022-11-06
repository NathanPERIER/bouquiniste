
from sources.base import Source
from core.models import ReleaseEntry, SourceInfo
from sources.collector import register
from sources.custom.manga_news.listing import ListingPage, getFirstListingPage, getNextListingPage
from sources.custom.manga_news.details import findDetails
from utils.iterables.multiple_months import MultiMonthsIterable
from utils.iterables.one_month import OneMonthIterable
from utils.wrappers import FlattenIterator

from datetime import date
from typing import Iterable, Sequence

@register("manga_news")
class MangaNewsSource(Source) :

	def getEntries(self, begin: date, end: date) -> "Iterable[ReleaseEntry]" :
		if begin.month == end.month and begin.year == end.year :
			return FlattenIterator(MN_OneMonthIterable(begin.month, begin.year, begin.day, end.day))
		return FlattenIterator(MN_MultiMonthsIterable(begin, end))

	def refineEntry(self, entry: ReleaseEntry) :
		findDetails(entry)
	
	def getInfo(self) -> SourceInfo :
		res = SourceInfo()
		res.name = 'Manga news'
		res.image = 'https://www.manga-news.com/mn-icon.png'
		return res


class MN_OneMonthIterable(OneMonthIterable[ListingPage,ReleaseEntry]) :

	def __init__(self, month: int, year: int, begin_day: int, end_day: int):
		super().__init__(month, year, begin_day, end_day)
	
	def firstInMonth(self) -> ListingPage : 
		return getFirstListingPage(self.month, self.year)

	def nextInMonth(self) -> "ListingPage | None" : 
		return getNextListingPage(self.page)

	def pageToEntrySequence(self, page: ListingPage) -> "Sequence[ReleaseEntry]" :
		return page.listing

	def entryToDay(self, entry: ReleaseEntry) -> int :
		return entry.release.day


class MN_MultiMonthsIterable(MultiMonthsIterable[ListingPage,ReleaseEntry]) :

	def __init__(self, begin: date, end: date) :
		super().__init__(begin, end)
	
	def firstInMonth(self) -> ListingPage : 
		return getFirstListingPage(self.current.month, self.current.year)

	def nextInMonth(self) -> "ListingPage | None" : 
		return getNextListingPage(self.page)

	def pageToEntrySequence(self, page: ListingPage) -> "Sequence[ReleaseEntry]" :
		return page.listing

	def entryToDate(self, entry: ReleaseEntry) -> date :
		return entry.release
	