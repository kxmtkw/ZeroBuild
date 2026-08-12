import subprocess
from pathlib import Path
from zero.errors import ZeroCompilationError, ZeroCompilationWarning

from zero.compilers.base import BaseCompilerDriver
from zero.compilers.msvc_cmd import MsvcCommandGenerator


class MsvcCompiler(BaseCompilerDriver):
	"""
	Compiler Driver for Microsoft Visual C++ (cl.exe).
	"""


	def __init__(self) -> None:
		super().__init__()
		self.binary = "cl.exe"
		self.msvc_cmd = MsvcCommandGenerator()


	def _parseDependencies(self, msvc_output: str) -> list[Path]:

		deps: list[Path] = []
		# "Note: including file:  <path>" (or localized equivalents containing the prefix pattern)
		for line in msvc_output.splitlines():
			if ":" in line and "including file" in line:
				_, path_str = line.split(":", 2)[1:] if line.count(":") >= 2 else line.split(":", 1)
				clean_path = path_str.strip()
				if clean_path:
					deps.append(Path(clean_path))
		return deps


	def getDependencies(self, filepath: Path, *, include_dirs: list[Path] = []) -> list[Path]:
		cmd = self.msvc_cmd.getDependencies(self.binary, filepath, include_dirs=include_dirs)

		process = subprocess.run(
			cmd,
			capture_output=True,
			text=True
		)

		if process.returncode != 0:
			raise ZeroCompilationError(str(filepath), process.stderr)

		return self._parseDependencies(process.stdout)


	def buildFile(
		self,
		filepath: Path,
		outfile: Path,
		*,
		for_shared: bool = False,
		include_dirs: list[Path] = [],
		arguments: list[str] = []
	) -> None:
		
		cmd = self.msvc_cmd.buildFile(
			self.binary,
			filepath,
			outfile,
			for_shared=for_shared,
			include_dirs=include_dirs,
			arguments=arguments
		)

		process = subprocess.run(
			cmd,
			capture_output=True,
			text=True,
			errors="replace"
		)

		if process.returncode != 0:
			raise ZeroCompilationError(str(filepath), process.stderr)

		if len(process.stderr) > 0:
			raise ZeroCompilationWarning(str(filepath), process.stderr)


	def buildStaticLib(self, objects: list[Path], outfile: Path) -> None:
		cmd = self.msvc_cmd.buildStaticLib(self.binary, objects, outfile)

		process = subprocess.run(
			cmd,
			capture_output=True,
			text=True,
			errors="replace"
		)

		if process.returncode != 0:
			raise ZeroCompilationError(outfile.name, process.stderr)

		if len(process.stderr) > 0:
			raise ZeroCompilationWarning(outfile.name, process.stderr)


	def buildSharedLib(self, objects: list[Path], libraries: list[Path], outfile: Path) -> None:
		cmd = self.msvc_cmd.buildSharedLib(self.binary, objects, libraries, outfile)

		process = subprocess.run(
			cmd,
			capture_output=True,
			text=True,
			errors="replace"
		)

		if process.returncode != 0:
			raise ZeroCompilationError(outfile.name, process.stderr)

		if len(process.stderr) > 0:
			raise ZeroCompilationWarning(outfile.name, process.stderr)


	def buildExecutable(self, objects: list[Path], libraries: list[Path], outfile: Path) -> None:
		cmd = self.msvc_cmd.buildExecutable(self.binary, objects, libraries, outfile)

		process = subprocess.run(
			cmd,
			capture_output=True,
			text=True,
			errors="replace"
		)

		if process.returncode != 0:
			raise ZeroCompilationError(outfile.name, process.stderr)

		if len(process.stderr) > 0:
			raise ZeroCompilationWarning(outfile.name, process.stderr)