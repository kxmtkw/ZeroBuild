import platform
from pathlib import Path


class TargetNameGenerator():
	"""
	Helper class to generate target names.
	"""

	def __init__(self) -> None:
		self._os = platform.system().lower()


	def objectFile(self, directory: Path, name: str) -> Path:
		"Generate an object file path. For convenience, we only append .o extension."
		return directory / (name + ".o")


	def staticLib(self, directory: Path, name: str) -> Path:
		"""
		Generate a static library / archive file path. 
		For a lib 'foo', 'libfoo.a' is obtained irrespective of os.
		"""
		return directory / ("lib" + name + ".a")


	def sharedLib(self, directory: Path, name: str) -> tuple[Path, Path]:
		"""
		Generate a shared library file path. 
		The first path is the location of the shared library while the second path indicates the path to link against.
		For linux and macos, both items are the same path.
		"""
		if self._os == "linux":
			path = directory / ("lib" + name + ".so")
			return (path, path)
		elif  self._os == "darwin":
			path = directory / ("lib" + name + ".dylib")
			return (path, path)
		else:
			# we assume only windows will be here for now.
			dll_path = directory / ( name + ".dll")
			lib_path = directory / ( name + ".lib")
			return (dll_path, lib_path)


	def executable(self, directory: Path, name: str) -> Path:
		"""
		Generate an executable file path. 
		"""
		if self._os == "linux" or self._os == "darwin":
			return directory / name
		else:
			# we assume only windows will be here for now.
			return directory / ( name + ".exe")
