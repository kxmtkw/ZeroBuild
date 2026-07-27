import json
from pathlib import Path
from typing import Any


class CacheManager:


	def __init__(self, filepath: Path) -> None:
		self._filepath = filepath
		self._data: dict[str, Any] = {}


	def load(self) -> bool:

		if not self._filepath.exists():
			self._filepath.parent.mkdir(parents=True, exist_ok=True)
			self._filepath.touch()
			self._data = {}
			return False

		try:
			with open(self._filepath) as file:
				self._data = json.load(file)
				if not isinstance(self._data, dict):
					self._data = {}
					return False
		except (json.JSONDecodeError, IsADirectoryError):
			self._data = {}
			return False

		return True

	def save(self) -> bool:
		"""Writes current cache data to the JSON file safely using atomic replacement."""
		try:
			self._filepath.parent.mkdir(parents=True, exist_ok=True)
			
			with open(self._filepath, "w", encoding="utf-8") as file:
				json.dump(self._data, file, indent=4)

			return True
		
		except (OSError, TypeError, ValueError):
			return False

	def get(
		self,
		*keypath: str,
		default: Any = None,
		valid_classes: tuple[type, ...] = ()
	) -> Any:

		if not keypath:
			return default

		current = self._data
		for key in keypath:
			if isinstance(current, dict) and key in current:
				current = current[key]
			else:
				return default

		if valid_classes and not isinstance(current, valid_classes):
			return default

		return current


	def set(self, *keypath: str, value: Any) -> None:

		if not keypath:
			raise ValueError("Keypath cannot be empty.")

		current = self._data
		for key in keypath[:-1]:
			if key not in current or not isinstance(current[key], dict):
				current[key] = {}
			current = current[key]

		current[keypath[-1]] = value