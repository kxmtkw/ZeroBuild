
from zero.compilers.get import getCompiler
from zero.compilers.get import getCompiler
from zero.compilers.types import CompilerType
from zero.errors.errors import ZeroAPIError
from zero.interface.source import Source
from zero.interface.library import Library

from zero.compilers.base import BaseCompiler

from zero.interface.build import Build

class Target:
	"""
	Base class to represent a target.
	Should not be created manually.
	"""

	def __init__(self, **kwargs,) -> None:
		self._linked_libs: list[Library] = []
		self._arguments: list[str] = []
		
		self._name: str
		self._source: Source
		self._compiler: CompilerType = "inherit"
		self._compiler_object: BaseCompiler


	def _validate(self, build: Build) -> None:
		
		if not hasattr(self, "_source"):
			raise ZeroAPIError(f"Source has not been specified for target [bold]{getattr(self, "_name", "unknown")}[/bold].")

		try:	
			self._compiler_object = build._compiler_object if self._compiler == "inherit" else getCompiler(self._compiler)
		except ValueError:
			raise ZeroAPIError(f"Unknown compiler specified for target [bold]{getattr(self, '_name', 'unknown')}[/bold]: '{self._compiler}'")

		if not self._compiler_object.doesExist():
			raise ZeroAPIError(f"Compiler '{self._compiler}' not found in PATH for target [bold]{getattr(self, '_name', 'unknown')}[/bold]'.")

		for lib in self._linked_libs:
			if not isinstance(lib, Library):
				raise ZeroAPIError(f"Linked library '{lib}' is not an instance of Library for target [bold]{getattr(self, '_name', 'unknown')}[/bold].")
		

	@property
	def name(self):
		"""
		Get the name of the target. If not assigned by the user, this propery will be automatically assigned to the variable name.
		Cannot be accessed if not manually assigned.
		"""
		if not hasattr(self, "_name"):
			raise ZeroAPIError("Name has not been specified for this target yet.")
		return self._name
	

	@name.setter
	def name(self, name: str):
		if name == "":
			raise ZeroAPIError("Target name cannot be an empty string.")
		self._name = name


	@property
	def source(self):
		"Specify the source files for the executable. Can only be set once."	
		return self._source
	

	@source.setter
	def source(self, src: Source):
		self._source = src

	
	@property
	def arguments(self):
		return self._arguments
	
	
	@arguments.setter
	def arguments(self, args: tuple[str, ...] | str):
		if isinstance(args, (tuple)):
			self._arguments = [arg for arg in args]
		else:
			self._arguments = [args]


	@property
	def compiler(self):
		"Manually set the compiler for this target. By default, the target inherits from Build."
		return self._compiler
	

	@compiler.setter
	def compiler(self, compiler: CompilerType):
		self._compiler = compiler


	def link(self, library: Library):
		"Link a library to this target."
		self._linked_libs.append(library)


	@property
	def linkedLibs(self):
		"Libraries linked against this target."
		return self._linked_libs