from .gcc import GccCompiler

class ClangxxCompiler(GccCompiler):
	"""
	Compiler Driver for clang++ compiler.
	"""
	def __init__(self) -> None:
		super().__init__()
		self.binary = "clang++"
