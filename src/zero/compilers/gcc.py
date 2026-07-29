from pathlib import Path
import subprocess
from zero.errors import ZeroCompilationError, ZeroCompilationWarning
from .base import BaseCompiler


class GccCompiler(BaseCompiler):


	def __init__(self) -> None:
		super().__init__()
		self.compiler_binary = self.linker_binary = "gcc"


	def _parseDependencies(self, gcc_output: str) -> list[Path]:
		cleaned = gcc_output.replace("\\\n", " ").replace("\\", " ")
		
		if ":" not in cleaned:
			return []
		
		_, deps_part = cleaned.split(":", 1)
		filepaths = deps_part.strip().split()
		filepaths.pop(0)
		
		return [Path(p) for p in filepaths]


	def getDependencies(self, filepath: Path, *, include_dirs: list[Path] = []) -> list[Path]:
		
		include_args = [f"-I{str(dir)}" for dir in include_dirs]

		process = subprocess.run(
			[self.compiler_binary, "-MM", *include_args, str(filepath)], 
			capture_output=True, 
			text=True
		)

		if process.returncode != 0:
			raise ZeroCompilationError(process.stderr)
		
		return self._parseDependencies(process.stdout)


	def buildFile(self, filepath: Path, outfile: Path, *, for_shared = False, include_dirs: list[Path] = [], arguments: list[str] = []) -> None:  

		include_args = [f"-I{str(dir)}" for dir in include_dirs]

		cmd = [self.compiler_binary, *arguments, "-c", *include_args, str(filepath), "-o", str(outfile)] 

		if for_shared:
			cmd.append("-fPIC")

		process = subprocess.run(
			cmd,
			capture_output=True, 
			text=True
		)

		if process.returncode != 0:
			raise ZeroCompilationError(process.stderr)

		if len(process.stderr) > 0:
			raise ZeroCompilationWarning(process.stderr)

		
	def buildStaticLib(self, objects: list[Path], outfile: Path) -> None:  
		
		str_objects = [str(obj) for obj in objects]

		process = subprocess.run(
			["ar", "rcs", str(outfile), *str_objects], 
			capture_output=True, 
			text=True
		)

		if process.returncode != 0:
			raise ZeroCompilationError(process.stderr)

		if len(process.stderr) > 0:
			raise ZeroCompilationWarning(process.stderr)
		

	def buildSharedLib(self, objects: list[Path], libraries: list[Path], outfile: Path) -> None:  
		
		str_objects = [str(obj) for obj in objects]
		
		cmd = [self.compiler_binary, "-shared", "-o", str(outfile), *str_objects]
		
		if libraries:
			cmd.append("-Wl,--whole-archive")
			for lib in libraries:
				cmd.append(str(lib))
			cmd.append("-Wl,--no-whole-archive")

		process = subprocess.run(
			cmd, 
			capture_output=True, 
			text=True
		)

		if process.returncode != 0:
			raise ZeroCompilationError(process.stderr)

		if len(process.stderr) > 0:
			raise ZeroCompilationWarning(process.stderr)


	def buildExecutable(self, objects: list[Path], libraries: list[Path], outfile: Path) -> None:  
		
		str_objects = [str(obj) for obj in objects]
		str_libs = [str(lib) for lib in libraries]

		process = subprocess.run(
			[self.compiler_binary, *str_objects, *str_libs, "-o", str(outfile)], 
			capture_output=True, 
			text=True
		)

		if process.returncode != 0:
			raise ZeroCompilationError(process.stderr)

		if len(process.stderr) > 0:
			raise ZeroCompilationWarning(process.stderr)