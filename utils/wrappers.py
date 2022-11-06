
from typing import Iterator, Iterable, Mapping, Sequence, TypeVar, Optional


T  = TypeVar('T')
KT = TypeVar('KT')
VT = TypeVar('VT')

class ErrorlessMapping(Mapping[KT,VT]) :

	def __init__(self, mapping: Mapping[KT,VT]) :
		self.mapping = mapping

	def __len__(self) -> int :
		return self.mapping.__len__()
	
	def __iter__(self) -> Iterator[KT] :
		return self.mapping.__iter__()

	def __contains__(self, key: KT):
		return self.mapping.__contains__(key)

	def __getitem__(self, key: KT) -> Optional[VT] :
		if key not in self.mapping :
			return None
		return self.mapping.__getitem__(key)


class FlattenIterator(Iterator[T]) :

	def __init__(self, wrapped: Iterable[Sequence[T]]) :
		self.iterator = iter(wrapped)
		self.seq: Sequence[T] = []
		self.index: int = 0
	
	def __next__(self) -> T :
		while self.index >= len(self.seq) :
			self.seq = next(self.iterator)
			self.index = 0
		res = self.seq[self.index]
		self.index += 1
		return res
