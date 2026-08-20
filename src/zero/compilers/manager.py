from functools import cache
from typing import Literal

from zero.compilers.base import BaseCompilerDriver
from zero.compilers.clang import ClangCompiler
from zero.compilers.clangxx import ClangxxCompiler
from zero.compilers.gcc import GccCompiler
from zero.compilers.gxx import GxxCompiler
from zero.compilers.msvc import MsvcCompiler

from zero.compilers.types import CompilerType, UsableCompilerType

_COMPILERS = {
	"gcc": GccCompiler(),
	"g++": GxxCompiler(),
	"clang": ClangCompiler(),
	"clang++": ClangxxCompiler(),
	"msvc": MsvcCompiler()
}


class CompilerManager:


	@staticmethod
	def getCompiler(compiler: UsableCompilerType, default: BaseCompilerDriver | None = None) -> BaseCompilerDriver:

		try:
			return _COMPILERS[compiler]
		except KeyError:
			if default is None:
				raise ValueError(f"Unsupported compiler driver: '{compiler}'")
			return default

		
	@staticmethod
	def getCompilerName(compiler: BaseCompilerDriver) -> str:

		for key, val in _COMPILERS.items():
			if val == compiler:
				return key

		return "unknown"


	@staticmethod
	def addCompiler(name: str, compiler: BaseCompilerDriver) -> None:
		_COMPILERS[name] = compiler
		