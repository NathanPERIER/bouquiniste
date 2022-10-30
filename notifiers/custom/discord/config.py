
from notifiers.base import NotifierConfig
from utils.wrappers import ErrorlessMapping
from utils.exceptions import BadConfigException

from typing import Mapping, Any


RELEASES_CHANNEL_FIELD = 'releases_channel'
FLOOD_CHANNEL_FIELD = 'flood_channel'
ADMIN_CHANNEL_FIELD = 'admin_channel'

class DiscordNotifierConfig(NotifierConfig) :

	def __init__(self, data: "Mapping[str,Any]") :
		wrapped = ErrorlessMapping(data)
		releases = wrapped[RELEASES_CHANNEL_FIELD]
		if releases is None :
			raise BadConfigException(f"Expected non-null URL for field `{RELEASES_CHANNEL_FIELD}`")
		self.releases: str = releases
		self.flood: "str | None" = data[FLOOD_CHANNEL_FIELD]
		self.admin: "str | None" = data[ADMIN_CHANNEL_FIELD]
