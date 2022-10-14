
from utils.bs4.base import BS4Node

class SelectorNotFoundException(Exception) :

	def __init__(self, selector: str, node: BS4Node) :
		super().__init__(f"No tag found matching selector {selector}\n{node.getBS4Trace()}")
