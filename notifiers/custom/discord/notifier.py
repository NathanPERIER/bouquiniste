
from notifiers.base import Notifier
from notifiers.collector import register
from notifiers.custom.discord.config import DiscordNotifierConfig
from core.models import ReleaseEntry, PublicationStatus
from sources.base import SourceInfo
from utils.environment import AGENT_NAME
from utils.dates import dateToTimestamp, LOG_FORMAT

from discord_webhook import DiscordWebhook, DiscordEmbed

from datetime import datetime


@register("discord", DiscordNotifierConfig)
class DiscordNotifier(Notifier) :

	def __init__(self, config: DiscordNotifierConfig) :
		self.config = config
	
	def notifyRelease(self, release: ReleaseEntry, info: SourceInfo) :
		webhook = DiscordWebhook(url=self.config.releases)
		embed = DiscordEmbed()
		embed.set_author(name=f"{AGENT_NAME} via {info.name}", url=release.link, icon_url=info.image)
		embed.set_title(release.title)
		if release.image is not None :
			embed.set_image(url=release.image)
		fields = {
			'Author': release.author,
			'Editor': release.editor,
			'Pages': release.pages,
			'Expected price': release.price
		}
		text = "\n".join(
			f"**{prop}**: {value}"
			for prop, value in fields.items()
			if value is not None
		)
		if release.number is not None :
			number_text = f"Tome {release.number}"
			if release.pub_status == PublicationStatus.FINISHED and release.pub_number is not None :
				number_text += f"/{release.pub_number}"
			text = f"{number_text}\n\n{text}" if len(text) > 0 else number_text
		if len(text) > 0 :
			embed.set_description(text)
		if release.isbn is not None :
			embed.set_footer(text = f"ISBN {release.isbn}")
		embed.set_timestamp(int(dateToTimestamp(release.release)))
		webhook.add_embed(embed)
		webhook.execute()
	
	def notifyError(self, error: Exception) :
		webhook = DiscordWebhook(url=self.config.admin)
		current_date = datetime.now().strftime(LOG_FORMAT)
		text = f"**[{current_date}]** {AGENT_NAME} received unexpected error of type `{type(error).__name__}`"
		error_str = str(error)
		if len(error_str) > 0 :
			text = f"{text}\n```\n{error_str}\n```"
		webhook.set_content(text)
		webhook.execute()
	


