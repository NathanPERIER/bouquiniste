
from .base import *
from .collector import sources as __b_sources
from utils.exceptions import BadConfigException

from sources.custom.manga_news.source import *

def getSource(source_id: str) -> Source :
	if source_id not in __b_sources :
		raise BadConfigException(f"No source associated with identifier {source_id}")
	source_cls, info = __b_sources[source_id]
	return source_cls(info)
