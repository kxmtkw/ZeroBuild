from pathlib import Path
from zero.errors.errors import ZeroAPIError


class Source:
	"""
	Specify source files for a target.
	Source files can both of the string or path objects.
	"""

	def __init__(self, *files: str | Path) -> None:

		self._sources_paths: list[Path] = []

		for f in files:

			if isinstance(f, str):
				p = Path(f)
			elif isinstance(f, Path):
				p = f
			else:
				raise ZeroAPIError(TypeError, f"Expected str or Path object. Got {type(f)}")

			if not p.exists():
				raise ZeroAPIError(FileNotFoundError, f"Source file not found: {str(p)}")
			
			self._sources_paths.append(p)
