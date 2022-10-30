
from core.models import ReleaseEntry

from typing import Sequence, Mapping, Any


class NotifierConfig :

	def __init__(self, data: "Mapping[str,Any]") :
		pass


class Notifier :

	def __init__(self, config: NotifierConfig) :
		pass

	def notifyImportantRelease(self, release: ReleaseEntry) :
		raise NotImplementedError()

	def notifyUnregisteredReleases(self, releases: "Sequence[ReleaseEntry]") :
		raise NotImplementedError()

	def notifyError(self, error: Exception) :
		raise NotImplementedError()
