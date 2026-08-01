from pathlib import Path
from typing import Literal

from zero.compilers.base import BaseCompiler
from zero.compilers.get import getCompiler
from zero.compilers.types import CompilerType
from zero.errors.errors import ZeroAPIError



class Build:
	"""
	Core class to make the build system.
	"""


	def __init__(self) -> None:
		self._directory: Path = Path("build")
		self._compiler: CompilerType | None = None
		self._compiler_object: BaseCompiler


	def _validate(self) -> None:
		
		if self._compiler is None:
			raise ZeroAPIError("Compiler has not been specified for the build system.")
		
		try:
			self._compiler_object = getCompiler(self._compiler)
		except ValueError:
			raise ZeroAPIError(f"Unknown compiler specified for build: '{self._compiler}'")

		if not self._compiler_object.doesExist():
			raise ZeroAPIError(f"Compiler '{self._compiler}' not found in PATH for build system.")

		
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
