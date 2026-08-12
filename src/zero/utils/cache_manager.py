import json
from pathlib import Path
from typing import Any


class CacheManager:

	_cache: dict[Path, dict[str, Any]] = {}

	def __init__(self, filepath: Path) -> None:
		self._filepath = filepath

		if filepath in CacheManager._cache:
			self._data = CacheManager._cache[filepath]
		else:
			self._data = self.load()
			CacheManager._cache[filepath] = self._data


	def load(self) -> dict[str, Any]:
		
		if not self._filepath.exists():
			self._filepath.parent.mkdir(parents=True, exist_ok=True)
			self._filepath.touch()
			return {}

		try:
			with open(self._filepath) as file:
				data = json.load(file)
				if not isinstance(data, dict):
					return {}
				return data
		except (json.JSONDecodeError, IsADirectoryError):
			return {}


	def reload(self):
		
		self._data = self.load()
		CacheManager._cache[self._filepath] = self._data

		
	def save(self) -> bool:

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


	def set(self, *keypath: str, value: Any) -> Any:

		if not keypath:
			raise ValueError("Keypath cannot be empty.")

		current = self._data
		for key in keypath[:-1]:
			if key not in current or not isinstance(current[key], dict):
				current[key] = {}
			current = current[key]

		current[keypath[-1]] = value

		return value


	def moveData(self, other: CacheManager):
		self._data = other._data.copy()


	def clear(self):
		self._data = {}
		self.save()