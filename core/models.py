
from datetime import date

class ListItem :
	def __init__(self) :
		self.link: str
		self.title: str
		self.image: "str | None"  = None
		self.number: "int | None" = None
		self.editor: "str | None" = None
		self.release: date

class ReleaseEntry :
	def __init__(self) :
		pass
