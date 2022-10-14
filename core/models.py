
from datetime import date

class ReleaseEntry :
	def __init__(self) :
		self.link: str
		self.title: str
		self.image: "str | None"  = None
		self.number: "int | None" = None
		self.editor: "str | None" = None
		self.release: date
		self.price: "str | None" = None
		self.pages: "int | None" = None
		self.status: "str | None" = None
		self.pub_country: "str | None" = None
		self.pub_number: "int | None" = None
		self.pub_status: "str | None" = None