
from notifiers.base import NotifierConfig
from utils.exceptions import BadConfigException

from typing import Mapping, Any


RELEASES_CHANNEL_FIELD = 'releases_channel'
ADMIN_CHANNEL_FIELD = 'admin_channel'

class DiscordNotifierConfig(NotifierConfig) :

	def __init__(self, data: "Mapping[str,Any]") :
		for field in [RELEASES_CHANNEL_FIELD, ADMIN_CHANNEL_FIELD] :
			if field not in data :
				raise BadConfigException(f"Expected non-null URL for field `{field}`")
		self.releases: str = data[RELEASES_CHANNEL_FIELD]
		self.admin: str = data[ADMIN_CHANNEL_FIELD]
