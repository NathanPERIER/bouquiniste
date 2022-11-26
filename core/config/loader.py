
from core.config import creation
from core.config.definitions import NOTIFIERS_FILE, SOURCES_FILE, ConfiguredSource
from notifiers import Notifier, getNotifier
from sources import getSource
from database import queries
from utils.exceptions import BadConfigException

import json
from sqlite3 import Cursor
from typing import Mapping, Any

__all__ = [
	"load"
]


def loadJson(path: str) -> Any :
	with open(path, 'r') as f :
		return json.load(f)


def load(cur: Cursor) -> "Mapping[str,ConfiguredSource]" :
	creation.init()
	res: "Mapping[str,ConfiguredSource]" = {}
	notifiers = __b_loadNotifiers()
	sources_config: "Mapping[str,Mapping[str,Any]]" = loadJson(SOURCES_FILE)
	for source_id, source_cfg in sources_config.items() :
		cs = ConfiguredSource(source_id)
		cs.source = getSource(source_cfg['type'])
		cs.notifiers = []
		for notifier_id in set(source_cfg['notifiers']) :
			if notifier_id not in notifiers :
				raise BadConfigException(f"Unknown notifier id {notifier_id}")
			cs.notifiers.append(notifiers[notifier_id])
		if len(cs.notifiers) == 0 :
			raise BadConfigException('All sources must use at least one notifier')
		cs.ids = queries.getFollowedSeries(cur, source_id)
		res[source_id] = cs
	return res


def __b_loadNotifiers() -> "Mapping[str,Notifier]" :
	notifiers_conf : "Mapping[str,Mapping[str,Any]]" = loadJson(NOTIFIERS_FILE)
	return {
		notifier_id: getNotifier(config['type'], config['config'])
		for notifier_id, config in notifiers_conf.items()
	}
	