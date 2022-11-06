from sources.base import Source

import logging
from typing import Type, Callable, Mapping

logger = logging.getLogger(__name__)

sources: "Mapping[str,Type[Source]]" = {}


def register(source_id: str) -> "Callable[[Type[Source]],Type[Source]]" :
	logger.debug("Registered source %s", source_id)
	def decorator(cls: "Type[Source]") -> "Type[Source]" :
		sources[source_id] = cls
		return cls
	return decorator
