import os
import platform
import shutil
import sys
from pathlib import Path


class System:
	"""
	Static class exposing system related utilities.
	"""

	def __init__(self) -> None:
		pass


	@classmethod
	def platform(cls) -> str:
		"""Get the host platform in which this build script will be run."""
		return sys.platform


	@classmethod
	def isLinux(cls) -> bool:
		"""Check whether the OS is linux."""
		return sys.platform.startswith("linux")


	@classmethod
	def isWindows(cls) -> bool:
		"""Check whether the OS is windows."""
		return sys.platform == "win32"


	@classmethod
	def isMacos(cls) -> bool:
		"""Check whether the OS is macos."""
		return sys.platform == "darwin"


	@classmethod
	def arch(cls) -> str:
		"""
		Return a normalized name of the architecture on which this script is running.
		Can be: 'x86_64', 'arm64', 'x86'.
		"""
		machine = platform.machine().lower()

		if machine in ("amd64", "x86_64"):
			return "x86_64"
		if machine in ("arm64", "aarch64"):
			return "arm64"
		if machine in ("i386", "i686", "x86"):
			return "x86"

		return machine


	@classmethod
	def environment(cls, name: str, *, default: str | None = None) -> str | None:
		"""Get an environment variable."""
		return os.environ.get(name, default)


	@classmethod
	def hasTool(cls, name: str) -> bool:
		"""Check whether an executable binary with the given name exists on the system."""
		return shutil.which(name) is not None


	@classmethod
	def getTool(cls, name: str) -> Path | None:
		"""Return an executable binary path as a Path object if found on the system. None otherwise."""
		path = shutil.which(name)
		return Path(path) if path is not None else None