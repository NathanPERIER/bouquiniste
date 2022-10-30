
from typing import Iterator, Sequence, Generic, TypeVar
from abc import ABC, abstractmethod

T  = TypeVar('T')
V  = TypeVar('V')

class OneMonthIterable(ABC,Generic[V,T],Iterator[Sequence[T]]) :

	def __init__(self, month: int, year: int, begin_day: int, end_day: int) :
		self.month = month
		self.year = year
		self.begin_day = begin_day
		self.end_day = end_day
		self.found_any = False
		self.none_left = False
		self.page: V = self.firstInMonth()
	
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
	def entryToDay(self, entry: T) -> int :
		pass 

	def __next__(self) -> "Sequence[T]" :
		if self.none_left :
			raise StopIteration
		if not self.found_any :
			return self.nextBeforeFind()
		return self.nextAfterFind()
	
	def filterUpperBound(self, seq: "Sequence[T]") -> "Sequence[T]" :
		res = [
			x for x in seq
			if self.entryToDay(x) <= self.end_day
		]
		if len(res) < len(seq) :
			self.none_left = True
		else :
			self.trySwitchPage()
		return res
	
	def trySwitchPage(self) :
		page = self.nextInMonth()
		if page is None :
			self.none_left = True
			return
		self.page = page

	def nextBeforeFind(self) -> "Sequence[T]" :
		filtered = [
			x for x in self.pageToEntrySequence(self.page)
			if self.entryToDay(x) >= self.begin_day
		]
		if len(filtered) > 0 :
			self.found_any = True
			return self.filterUpperBound(filtered)
		self.trySwitchPage()
		return filtered
	
	def nextAfterFind(self) -> "Sequence[T]" :
		return self.filterUpperBound(self.pageToEntrySequence(self.page))
