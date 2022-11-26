
from notifiers import Notifier
from sources import Source
from utils.paths import CONFIG_FOLDER

import os
from typing import Iterable, Sequence

NOTIFIERS_FILE = os.path.join(CONFIG_FOLDER, 'notifiers.json')
SOURCES_FILE = os.path.join(CONFIG_FOLDER, 'sources.json')

__all__ = [
	"ConfiguredSource"
]


class ConfiguredSource :
	def __init__(self, identifier: str) :
		self.identifier = identifier
		self.notifiers: "Iterable[Notifier]"
		self.source: Source
		self.ids: "Sequence[str]"
