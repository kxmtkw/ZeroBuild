from .gcc import GccCompiler

class ClangCompiler(GccCompiler):

	def __init__(self) -> None:
		super().__init__()
		self.binary = "clang++"
