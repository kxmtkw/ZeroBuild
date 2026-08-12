from dataclasses import dataclass, fields
from pathlib import Path


@dataclass(init=False)
class Directory:
	build: Path
	objects: Path
	lib: Path
	static_lib: Path
	shared_lib: Path
	binary: Path

	def create_all(self):
		for field in fields(self):
			path = getattr(self, field.name)
			path.mkdir(parents=True, exist_ok=True)


@dataclass(init=False)
class BuildConfig:
	"""
	Details about the Build configuration.
	"""
	directory: Directory
	fresh_build: bool
	threads: int
	build_script: Path
	build_script_updated: bool

