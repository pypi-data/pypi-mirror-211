class OpenOCR(object):
	"""docstring for OpenOCR"""
	def __init__(
		self,
		*,
		debug: bool = False,
		title: str = "OpenOCR",
		description: str = "",
		version: str = "0.0.2"
		) -> None:
		self.debug = debug
		self.title = title
		self.description = description
		self.version = version
		