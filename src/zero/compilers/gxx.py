from .gcc import GccCompiler

class GxxCompiler(GccCompiler):

	def __init__(self) -> None:
		super().__init__()
		self.binary = "clang++"
