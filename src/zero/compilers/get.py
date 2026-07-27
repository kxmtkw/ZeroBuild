from functools import cache
from typing import Literal

from zero.compilers.base import BaseCompiler
from zero.compilers.clang import ClangCompiler
from zero.compilers.clangxx import ClangxxCompiler
from zero.compilers.gcc import GccCompiler
from zero.compilers.gxx import GxxCompiler

from zero.compilers.types import CompilerType

_COMPILERS = {
	"gcc": GccCompiler(),
	"g++": GxxCompiler(),
	"clang": ClangCompiler(),
	"clang++": ClangxxCompiler(),
}

def getCompiler(compiler: CompilerType, default: BaseCompiler | None = None) -> BaseCompiler:
	try:
		return _COMPILERS[compiler]
	except KeyError:
		if default is None:
			raise ValueError(f"Unsupported compiler driver: '{compiler}'")
		return default

def getCompilerName(compiler: BaseCompiler) -> str:
	for key, val in _COMPILERS.items():
		if val == compiler:
			return key

	return "unknown"