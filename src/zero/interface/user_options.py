from typing import Any


class UserOptions:

	
	def __init__(self) -> None:
		pass


	@classmethod
	def get(cls, name: str, *, default: str | None = None) -> str | None:
		"Get a user specified option."
		val = getattr(cls, name, default)
		return val


	@classmethod
	def defined(cls, name: str) -> bool:
		"Check whether a option was defined."
		return hasattr(cls, name)

