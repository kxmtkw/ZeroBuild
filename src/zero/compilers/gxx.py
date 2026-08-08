from .gcc import GccCompiler

class GxxCompiler(GccCompiler):
	"""
	Compiler Driver for g++ compiler.
	"""
	def __init__(self) -> None:
		super().__init__()
		self.binary = "g++"
