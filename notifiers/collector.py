from notifiers.base import Notifier, NotifierConfig

from typing import Type, Callable, Mapping, Tuple

notifiers: "Mapping[str,Tuple[Type[Notifier],Type[NotifierConfig]]]" = {}

def register(notifier_id: str, config_class: "Type[NotifierConfig]") -> "Callable[[Type[Notifier]],Type[Notifier]]" :
	def decorator(cls: "Type[Notifier]") -> "Type[Notifier]" :
		notifiers[notifier_id] = (cls, config_class)
		return cls
	return decorator
