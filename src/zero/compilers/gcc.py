from pathlib import Path
import subprocess
from zero.errors import ZeroCompilationError, ZeroCompilationWarning
from .base import BaseCompilerDriver
from .gcc_cmd import GccCommandGenerator


class GccCompiler(BaseCompilerDriver):
	"""
	Compiler Driver for gcc C compiler.
	Any compiler whose command structure matches gcc can simply inherit from from this class and change the `binary` field.
	For example, for a clang driver, it can inherit from this class and set `self.binary` to `clang`. 
	"""

	def __init__(self) -> None:
		super().__init__()
		self.binary = "gcc"
		self.gcc_cmd = GccCommandGenerator()


	def _parseDependencies(self, gcc_output: str) -> list[Path]:
		cleaned = gcc_output.replace("\\\n", " ").replace("\\", " ")
		
		if ":" not in cleaned:
			return []
		
		_, deps_part = cleaned.split(":", 1)
		filepaths = deps_part.strip().split()
		filepaths.pop(0)
		
		return [Path(p) for p in filepaths]


	def getDependencies(self, filepath: Path, *, include_dirs: list[Path] = []) -> list[Path]:
		
		cmd = self.gcc_cmd.getDependencies(self.binary, filepath, include_dirs=include_dirs)

		process = subprocess.run(
			cmd, 
			capture_output=True, 
			text=True
		)

		if process.returncode != 0:
			raise ZeroCompilationError(str(filepath), process.stderr)
		
		return self._parseDependencies(process.stdout)


	def buildFile(self, filepath: Path, outfile: Path, *, for_shared = False, include_dirs: list[Path] = [], arguments: list[str] = [], do_not_compile = False) -> list[str]:  

		cmd = self.gcc_cmd.buildFile(self.binary, filepath, outfile, for_shared=for_shared, include_dirs=include_dirs, arguments=arguments)

		if for_shared:
			cmd.append("-fPIC")

		if do_not_compile:
			return cmd

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

		return cmd

		
	def buildStaticLib(self, objects: list[Path], outfile: Path) -> None:  
		
		cmd = self.gcc_cmd.buildStaticLib(self.binary, objects, outfile)

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
		
		cmd = self.gcc_cmd.buildSharedLib(self.binary, objects, libraries, outfile)

		for lib in libraries:
			cmd.append("-Wl,--whole-archive")
			cmd.append(str(lib))
			cmd.append("-Wl,--no-whole-archive")

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

		cmd = self.gcc_cmd.buildExecutable(self.binary, objects, libraries, outfile)

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