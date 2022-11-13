
from core.config import checker
from core.config.definitions import NOTIFIERS_FILE, SOURCES_FILE, LISTS_FOLDER, ConfiguredSource
from notifiers import Notifier, getNotifier
from sources import getSource
from utils.exceptions import BadConfigException

import os
import json
from typing import Mapping, Sequence, Any


def loadJson(path: str) -> Any :
	with open(path, 'r') as f :
		return json.load(f)


def load() -> "Sequence[ConfiguredSource]" :
	checker.check()
	res: "Sequence[ConfiguredSource]" = []
	notifiers = __b_loadNotifiers()
	lists: "Mapping[str,Mapping[str,Sequence[str]]]" = {}
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
		if source_cfg['list'] in lists :
			list_conf = lists[source_cfg['list']]
		else :
			list_conf = __b_loadList(source_cfg['list'])
			lists[source_cfg['list']] = list_conf
		cs.names = list_conf['name']
		cs.ids = list_conf['id']
		res.append(cs)
	return res


def __b_loadNotifiers() -> "Mapping[str,Notifier]" :
	notifiers_conf : "Mapping[str,Mapping[str,Any]]" = loadJson(NOTIFIERS_FILE)
	return {
		notifier_id: getNotifier(config['type'], config['config'])
		for notifier_id, config in notifiers_conf.items()
	}

def __b_loadList(name: str) -> "Mapping[str,Sequence[str]]" :
	if name.startswith('/') :
		name = name[1:]
	path = os.path.join(LISTS_FOLDER, name + ".json")
	if not os.path.isfile(path) :
		raise BadConfigException(f"List {name} not found")
	return loadJson(path)
	
	