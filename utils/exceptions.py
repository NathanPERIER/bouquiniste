
class BadConfigException(Exception) :

	def __init__(self, message: str) :
		super().__init__(message)


class FormatException(Exception) :

	def __init__(self, message: str) :
		super().__init__(message)
