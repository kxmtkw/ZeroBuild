from zero.interface.headers import PrivateOnlyHeaders
from zero.interface.target import Target


class Executable(Target):
	"""
	Build an executable target.
	"""

	def __init__(self) -> None:
		super().__init__()
		self.headers = PrivateOnlyHeaders()