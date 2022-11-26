from sources.base import Source, SourceInfo

import logging
from typing import Type, Callable, Mapping, Tuple

logger = logging.getLogger(__name__)

sources: "Mapping[str,Tuple[Type[Source],SourceInfo]]" = {}


def register(source_id: str, info: SourceInfo) -> "Callable[[Type[Source]],Type[Source]]" :
	logger.debug("Registered source %s", source_id)
	def decorator(cls: "Type[Source]") -> "Type[Source]" :
		sources[source_id] = (cls, info)
		return cls
	return decorator
