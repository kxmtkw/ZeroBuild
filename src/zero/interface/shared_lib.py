from zero.interface.target import Target
from zero.interface.library import Library
from zero.interface.headers import Headers


class SharedLibrary(Target, Library):
	"""
	Build a shared library target.
	"""

	def __init__(self) -> None:
		super().__init__()
		self.headers = Headers()