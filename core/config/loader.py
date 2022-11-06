
from core.config import checker
from core.config.definitions import NOTIFIERS_FILE, SOURCES_FILE, LISTS_FOLDER, ConfiguredSource
from notifiers import Notifier, getNotifier
from sources import Source, getSource
from utils.exceptions import BadConfigException

import os
import json
from typing import Mapping, Sequence, Iterable, Any


def loadJson(path: str) -> Any :
	with open(path, 'r') as f :
		return json.load(f)


def load() -> "Iterable[ConfiguredSource]" :
	checker.check()
	res: "Iterable[ConfiguredSource]" = []
	notifiers = __b_loadNotifiers()
	lists: "Mapping[str,Sequence[str]]" = {}
	sources_config: "Sequence[Mapping[str,Any]]" = loadJson(SOURCES_FILE)
	for source_cfg in sources_config :
		cs = ConfiguredSource()
		cs.source = getSource(source_cfg['type'])
		cs.notifiers = []
		for notifier_id in set(source_cfg['notifiers']) :
			if notifier_id not in notifiers :
				raise BadConfigException(f"Unknown notifier id {notifier_id}")
			cs.notifiers.append(notifiers[notifier_id])
		if len(cs.notifiers) == 0 :
			raise BadConfigException('All sources must use at least one notifier')
		if source_cfg['list'] in lists :
			cs.list = lists[source_cfg['list']]
		else :
			lst = __b_loadList(source_cfg['list'])
			lists[source_cfg['list']] = lst
			cs.list = lst
		res.append(cs)
	return res


def __b_loadNotifiers() -> "Mapping[str,Notifier]" :
	notifiers_conf : "Mapping[str,Mapping[str,Any]]" = loadJson(NOTIFIERS_FILE)
	return {
		notifier_id: getNotifier(config['type'], config['config'])
		for notifier_id, config in notifiers_conf.items()
	}

def __b_loadList(name: str) -> "Sequence[str]" :
	if name.startswith('/') :
		name = name[1:]
	path = os.path.join(LISTS_FOLDER, name + ".json")
	if not os.path.isfile(path) :
		raise BadConfigException(f"List {name} not found")
	with open(path, 'r') as f :
		res = f.readlines()
	return [
		x for x in 
		(y.strip() for y in res)
		if not x.startswith('//')
	]
	