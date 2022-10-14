from sources.base import Source

from typing import Type, Callable
from collections.abc import Mapping

sources: "Mapping[str,Type[Source]]" = {}

def register(source_id: str) -> "Callable[[Type[Source]],Type[Source]]" :
	def decorator(cls: "Type[Source]") -> "Type[Source]" :
		sources[source_id] = cls
		return cls
	return decorator
