from pathlib import Path

from zero.compilers.base import BaseCompilerDriver
from zero.compilers.manager import CompilerManager
from zero.compilers.types import CompilerType

from zero.interface.types import FlagType
from zero.interface.internals import Internals

from zero.errors.errors import ZeroAPIError


class Build:
	"""
	Core class to configure the build system.
	Use it to set global/fallback compiler and arguments.

	Must be set to the variable `build` for Zero to detect it. Fails if not found.
	"""


	def __init__(self) -> None:
		self._directory: Path = Path("build")
		self._compiler: CompilerType | None = None
		self._compiler_object: BaseCompilerDriver
		self._arguments: list[str] = []
		self._export_compile_commands: bool = False


	def _validate(self) -> None:
		
		if self._compiler is None:
			raise ZeroAPIError("Compiler has not been specified for the build system.")
		
		try:
			self._compiler_object = CompilerManager.getCompiler(self._compiler)
		except ValueError:
			raise ZeroAPIError(f"Unknown compiler specified for build: '{self._compiler}'")

		if not self._compiler_object.doesExist():
			raise ZeroAPIError(f"Compiler '{self._compiler}' not found in PATH for build system.")

		
	@property
	def compiler(self):
		"""
		Specify a fallback compiler for the build system.
		Any target that does not specify a compiler will automatically inherit from this one.
		"""
		return self._compiler


	@compiler.setter
	def compiler(self, name: CompilerType):
		self._compiler = name


	@property
	def directory(self):
		"""
		Set a directory for the build system. 
		If not specified, defaults to ./build
		"""
		return self._directory


	@directory.setter
	def directory(self, name: str | Path):
		self._directory = Path(name)


	@property
	def arguments(self):
		"""
		Global arguments to be passed to the compiler for all targets in the build system.
		Not recommended if the build system has multiple languages or uses multiple compilers.
		Should only be used if the whole project uses the same compiler and the same language.
		"""
		return self._arguments


	@arguments.setter
	def arguments(self, args: tuple[FlagType, ...] | FlagType):
		if isinstance(args, (tuple)):
			self._arguments = [str(arg) for arg in args]
		else:
			self._arguments = [str(args)]


	@property
	def export_compile_commands(self):
		"""
		Whether to export `compile_commands.json` file which is used for intellisense.
		If turned on, will export the file whenever the build file updates.
		"""
		return self._export_compile_commands


	@export_compile_commands.setter
	def export_compile_commands(self, value: bool):
		self._export_compile_commands = value


	def addCompiler(self, name: str, compiler: Internals.CompilerDriver):
		"""
		Add a custom compiler driver to the build system.
		The driver can then be referred in the build system by the `name` value.
		Can overshadow existing compilers.
		"""
		CompilerManager.addCompiler(name, compiler)
