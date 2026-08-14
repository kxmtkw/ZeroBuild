from abc import ABC, abstractmethod
from pathlib import Path

from shutil import which


class BaseCompilerDriver(ABC):
	"""
	Base class for Compilers utilizing pathlib.Path objects.
	"""

	def __init__(self) -> None:
		super().__init__()
		self.binary: str = ""


	def doesExist(self) -> bool:
		return which(self.binary) is not None


	@abstractmethod
	def getDependencies(self, filepath: Path, *, include_dirs: list[Path] = []) -> list[Path]:
		pass


	@abstractmethod
	def buildFile(self, filepath: Path, outfile: Path, *, for_shared = False, include_dirs: list[Path] = [], arguments: list[str] = [], do_not_compile = False) -> list[str]:  
		pass
	

	@abstractmethod
	def buildStaticLib(self, objects: list[Path], outfile: Path) -> None:  
		pass


	@abstractmethod
	def buildSharedLib(self, objects: list[Path], libraries: list[Path], outfile: Path) -> None:  
		pass


	@abstractmethod
	def buildExecutable(self, objects: list[Path], libraries: list[Path], outfile: Path) -> None:  
		pass