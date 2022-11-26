
from enum import Enum
from datetime import date
from typing import Final


class PublicationStatus(Enum) :
	FINISHED = 'finished'
	ONGOING = 'ongoing'
	UNKNOWN = 'unknown'


class ReleaseEntry :
	def __init__(self, manga_id: str) :
		self.link: str
		self.title: str
		self.manga_id: Final[str] = manga_id
		self.series_id: "str | None" = None
		self.image: "str | None"  = None
		self.number: "int | None" = None
		self.editor: "str | None" = None
		self.author: "str | None" = None
		self.release: date
		self.isbn: "str | None" = None
		self.price: "str | None" = None
		self.pages: "int | None" = None
		self.status: PublicationStatus = PublicationStatus.UNKNOWN
		self.pub_status: PublicationStatus = PublicationStatus.UNKNOWN
		self.pub_number: "int | None" = None
