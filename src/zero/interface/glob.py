from pathlib import Path
import re

from zero.errors.errors import ZeroAPIError
from zero.interface.types import PathType


def _matches_pattern(filename: str, pattern: str) -> bool:
	try:
		return re.search(pattern, filename) is not None
	except re.error:
		return False

	
def FileGlob(directory: PathType, pattern: str | None = None):
	"""
	Get all files from a given directory that matches the given pattern.
	If no pattern is provided, it globs all files inside the directory.
	If you want to glob all .c files within a directory: FileGlob(directory, "*.c")
	"""

	if isinstance(directory, str):
		directory = Path(directory)

	if not directory.is_dir():
		raise ZeroAPIError(NotADirectoryError, f"{str(directory)} is not a directory.")

	files: list[Path] = []

	for item in directory.iterdir():

		if pattern is None:
			files.append(item)
			continue

		if item.is_file():
			if _matches_pattern(item.name, pattern):
				files.append(item)

	return files

