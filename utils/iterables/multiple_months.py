
from datetime import date
from dateutil.relativedelta import relativedelta
from typing import Iterator, Sequence, Generic, TypeVar
from abc import ABC, abstractmethod

T  = TypeVar('T')
V  = TypeVar('V')

ONE_MONTH_DELTA = relativedelta(months=1)

class MultiMonthsIterable(ABC,Generic[V,T],Iterator[Sequence[T]]) :
	
	def __init__(self, begin: date, end: date) :
		self.begin = begin
		self.end = end
		self.current = begin
		self.page = self.firstInMonth()
		self.last_month = False
		self.found_one = False
		self.reached_end = False
	
	@abstractmethod
	def firstInMonth(self) -> V : 
		pass

	@abstractmethod
	def nextInMonth(self) -> "V | None" : 
		pass

	@abstractmethod
	def pageToEntrySequence(self, page: V) -> "Sequence[T]" :
		pass 

	@abstractmethod
	def entryToDate(self, entry: T) -> date :
		pass 

	def nextPage(self) :
		# Try to get the next page for the current month
		page = self.nextInMonth()
		if page is not None :
			self.page = page
			return
		# If we reached the end of the month, try and switch to the next month
		if self.last_month :
			# If we're already in the last month, stop iterating
			# (happens if the last day of the range is the last day of the month)
			self.reached_end = True
			return
		self.found_one = True # Forces to leave the state when we probe for the beginning of the range
		self.current = self.current + ONE_MONTH_DELTA
		if self.current.month == self.end.month and self.current.year == self.end.year :
			self.last_month = True
		self.page = self.firstInMonth()
	
	def __next__(self) -> "Sequence[T]" :
		if self.reached_end :
			raise StopIteration
		if self.last_month :
			return self.nextNearEnd()
		if self.found_one :
			return self.nextWithinRange()
		return self.nextProbingBeginning()
	
	def nextProbingBeginning(self) -> "Sequence[T]" :
		res = [
			x for x in self.pageToEntrySequence(self.page)
			if self.entryToDate(x) >= self.begin
		]
		if len(res) > 0 :
			self.found_one = True
		self.nextPage()
		return res
	
	def nextWithinRange(self) -> "Sequence[T]" :
		res = self.pageToEntrySequence(self.page)
		self.nextPage()
		return res
	
	def nextNearEnd(self) -> "Sequence[T]" :
		listing = self.pageToEntrySequence(self.page)
		res = [
			x for x in listing
			if self.entryToDate(x) <= self.end
		]
		if len(res) < len(listing) :
			self.reached_end = True
		else :
			self.nextPage()
		return res
