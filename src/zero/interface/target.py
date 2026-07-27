
from zero.compilers.types import CompilerType
from zero.errors.errors import ZeroAPIError
from zero.interface.source import Source
from zero.interface.library import Library

from zero.compilers.base import BaseCompiler


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


	@property
	def name(self):
		"""
		Get the name of the target. If not assigned by the user, this propery will be automatically assigned to the variable name.
		Cannot be accessed if not manually assigned.
		"""
		if not hasattr(self, "_name"):
			raise ZeroAPIError(ValueError, "Name has not been specified for this target yet.")
		return self._name
	

	@name.setter
	def name(self, name: str):
		if name == "":
			raise ZeroAPIError(ValueError, "Target name cannot be an empty string.")
		self._name = name


	@property
	def source(self):
		"Specify the source files for the executable. Can only be set once."	

		if not hasattr(self, "_source"):
			raise ZeroAPIError(ValueError, "Source not specified for this target.")
			
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