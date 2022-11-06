
from notifiers.base import Notifier
from notifiers.collector import notifiers as __b_notifiers
from utils.exceptions import BadConfigException

from notifiers.custom.discord.notifier import DiscordNotifier

import logging
from typing import Mapping, Any


def getNotifier(notifier_id: str, config: Mapping[str, Any]) -> Notifier :
	if notifier_id not in __b_notifiers :
		raise BadConfigException(f"No notifier associated with identifier {notifier_id}")
	notifier_cls, conf_cls = __b_notifiers[notifier_id]
	conf = conf_cls(config)
	return notifier_cls(conf)
