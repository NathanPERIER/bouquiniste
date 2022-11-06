
from notifiers import Notifier
from sources import Source

import os
from typing import Iterable, Sequence

__THIS_FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

CONFIG_FOLDER = os.path.join(__THIS_FOLDER, 'config')
LISTS_FOLDER = os.path.join(CONFIG_FOLDER, 'lists')

NOTIFIERS_FILE = os.path.join(__THIS_FOLDER, 'notifiers.json')
SOURCES_FILE = os.path.join(__THIS_FOLDER, 'sources.json')


class ConfiguredSource :
	def __init__(self) :
		self.notifiers: "Iterable[Notifier]"
		self.source: Source
		self.list: "Sequence[str]"
