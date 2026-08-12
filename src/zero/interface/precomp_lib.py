from pathlib import Path

from zero.interface.headers import PublicOnlyHeaders
from zero.interface.library import Library


class PreCompiledLibrary(Library):
	"""
	Specify a Pre-compiled library. Can be both static or shared.

	For now, library lookup is not performed so you will have to manually specify the path of the library,
	along with the public headers it exposes.
	"""

	def __init__(self, filepath: str | Path) -> None:
		super().__init__()
		self.headers = PublicOnlyHeaders()
		self._filepath = Path(filepath)

	@property
	def filepath(self):
		return self._filepath