from zero.compilers.base import BaseCompilerDriver
from zero.compilers import *


class Internals:
	"""
	Static class exposing build system internals.
	"""

	class CompilerDriver(BaseCompilerDriver):
		"""
		Create a custom compiler driver. It must support all required methods to function.
		After creation, create the compiler driver and pass it to build.
		"""
		pass


	class Compilers:
		GccCompiler = GccCompiler
		GxxCompiler = GxxCompiler
		ClangCompiler = ClangCompiler
		ClangxxCompiler = ClangxxCompiler

