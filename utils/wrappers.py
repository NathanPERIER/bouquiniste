

from typing import Iterator, Mapping, TypeVar, Optional

KT = TypeVar('KT')
VT = TypeVar('VT')


class ErrorlessMapping(Mapping[KT,VT]) :

	def __init__(self, mapping: Mapping[KT,VT]) :
		self.mapping = mapping

	def __len__(self) -> int :
		return self.mapping.__len__()
	
	def __iter__(self) -> Iterator[KT] :
		return self.mapping.__iter__()

	def __getitem__(self, key: KT) -> Optional[VT] :
		if key not in self.mapping :
			return None
		return self.mapping.__getitem__(key)