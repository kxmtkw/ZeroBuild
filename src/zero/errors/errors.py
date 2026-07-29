import sys
import traceback

class ZeroError(Exception):
	"""
	Base class for all zero related errors.
	"""
	def __init__(self, *args: object) -> None:
		super().__init__(*args)
			

class ZeroAPIError(ZeroError):
	"""
	User errors related to the Zero API. For example, source file not found or unknown compiler.
	"""

	def __init__(self, error: str) -> None:
		super().__init__(error)


class ZeroCircularDependencyError(ZeroError):
	"""
	Circular dependency detected within the dependency graph.
	"""

	def __init__(self, error: str) -> None:
		super().__init__(error)


class ZeroCompilationError(ZeroError):
	"""
	Error during compilation.
	"""

	def __init__(self, cause: str, error: str) -> None:
		super().__init__(error)
		self.cause = cause
		self.error = error


class ZeroCompilationWarning(ZeroError):
	"""
	Warnings during compilation. Should not halt compilation.
	"""

	def __init__(self, cause: str, error: str) -> None:
			super().__init__(error)
			self.cause = cause
			self.error = error