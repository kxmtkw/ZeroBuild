from pathlib import Path
from typing import Literal

from zero.compilers.base import BaseCompiler
from zero.compilers.types import CompilerType
from zero.errors.errors import ZeroAPIError
from zero.interface.target import Target

from zero.interface.library import Library
from zero.interface.executable import Executable


class Build:
	"""
	Core class to make the build system.
	"""


	def __init__(self) -> None:
		self._targets: list[Target] = []
		self._directory: Path = Path("build")
		self._compiler: CompilerType | None = None
		self._compiler_object: BaseCompiler


	@property
	def compiler(self):
		"""
		Specify a compiler for the build system. 
		"""
		return self._compiler


	@compiler.setter
	def compiler(self, name: CompilerType):
		self._compiler = name


	@property
	def directory(self):
		"""
		Set a directory for the build system. If not specified, defaults to ./build
		"""
		return self._directory


	@directory.setter
	def directory(self, name: str | Path):
		self._directory = Path(name)
