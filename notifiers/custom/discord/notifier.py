
from notifiers.base import Notifier
from notifiers.collector import register
from notifiers.custom.discord.config import DiscordNotifierConfig
from core.models import ReleaseEntry

from typing import Sequence
from discord_webhook import DiscordWebhook


@register("discord", DiscordNotifierConfig)
class DiscordNotifier(Notifier) :

	def __init__(self, config: DiscordNotifierConfig) :
		self.config = config
	
	def notifyImportantRelease(self, release: ReleaseEntry) :
		webhook = DiscordWebhook(self.config.releases)
		raise NotImplementedError()

	def notifyUnregisteredReleases(self, releases: "Sequence[ReleaseEntry]") :
		if self.config.flood is None :
			return
		webhook = DiscordWebhook(self.config.flood)
		raise NotImplementedError()
	
	def notifyError(self, error: Exception) :
		if self.config.admin is None :
			return
		webhook = DiscordWebhook(self.config.admin)
		raise NotImplementedError()
	


