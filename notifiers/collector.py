from notifiers.base import Notifier, NotifierConfig

import logging
from typing import Type, Callable, Mapping, Tuple

logger = logging.getLogger(__name__)

notifiers: "Mapping[str,Tuple[Type[Notifier],Type[NotifierConfig]]]" = {}


def register(notifier_id: str, config_class: "Type[NotifierConfig]") -> "Callable[[Type[Notifier]],Type[Notifier]]" :
	logger.debug("Registered notifier %s", notifier_id)
	def decorator(cls: "Type[Notifier]") -> "Type[Notifier]" :
		notifiers[notifier_id] = (cls, config_class)
		return cls
	return decorator
