
from notifiers import Notifier
from sources import Source
from utils.paths import CONFIG_FOLDER

import os
from typing import Iterable, Sequence

LISTS_FOLDER = os.path.join(CONFIG_FOLDER, 'lists')
NOTIFIERS_FILE = os.path.join(CONFIG_FOLDER, 'notifiers.json')
SOURCES_FILE = os.path.join(CONFIG_FOLDER, 'sources.json')


class ConfiguredSource :
	def __init__(self, identifier: str) :
		self.identifier = identifier
		self.notifiers: "Iterable[Notifier]"
		self.source: Source
		self.names: "Sequence[str]"
		self.ids: "Sequence[str]"
