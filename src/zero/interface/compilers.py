from zero.compilers.manager import CompilerManager
from zero.compilers.types import UsableCompilerType
from zero.errors.errors import ZeroAPIError
from zero.interface.types import FlagType


class CompilerArguments:
	"""
	Specify the default arguments for individual compilers.
	"""

	def __init__(self) -> None:
		pass


	def __setitem__(self, key: UsableCompilerType, value: tuple[FlagType, ...] | FlagType):
		if isinstance(value, (tuple)):
			arguments = [str(arg) for arg in value]
		else:
			arguments = [str(value)]

		try:
			compiler = CompilerManager.getCompiler(key)
		except ValueError as e:
			raise ZeroAPIError(str(e))

		compiler.setBaseArguments(arguments)


	def __getitem__(self, key: UsableCompilerType) -> list[FlagType]:

		try:
			compiler = CompilerManager.getCompiler(key)
		except ValueError as e:
			raise ZeroAPIError(str(e))

		return compiler.base_arguments


class Compilers:

	def __init__(self) -> None:
		self._arguments = CompilerArguments()

	@property
	def arguments(self):
		"Specify base/default arguments for a compiler. Specify the compiler by the [] operator."
		return self._arguments
	