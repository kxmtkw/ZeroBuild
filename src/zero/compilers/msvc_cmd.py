from pathlib import Path


class MsvcCommandGenerator:
	"""
	Helper class to generate commands for MSVC (cl.exe and lib.exe).
	"""


	def __init__(self) -> None:
		pass


	def getDependencies(
		self,
		binary: str,
		filepath: Path,
		*,
		include_dirs: list[Path] = []
	) -> list[str]:
		# /E /P preprocesses to a file without compiling.
		include_args = [f"/I{str(d)}" for d in include_dirs]
		cmd = [binary, "/nologo", "/showIncludes", "/E", *include_args, str(filepath)]
		return cmd


	def buildFile(
		self,
		binary: str,
		filepath: Path,
		outfile: Path,
		*,
		for_shared: bool = False,
		include_dirs: list[Path] = [],
		arguments: list[str] = []
	) -> list[str]:
		
		include_args = [f"/I{str(d)}" for d in include_dirs]
		# /c compiles without linking
		cmd = [binary, "/nologo", *arguments, "/c", *include_args, str(filepath), f"/Fo{str(outfile)}"]
		return cmd


	def buildStaticLib(
		self,
		binary: str,
		objects: list[Path],
		outfile: Path
	) -> list[str]:
		
		str_objects = [str(obj) for obj in objects]

		if outfile.exists():
			outfile.unlink()

		cmd = ["lib.exe", "/nologo", f"/OUT:{str(outfile)}", *str_objects]
		return cmd


	def buildSharedLib(
		self,
		binary: str,
		objects: list[Path],
		libraries: list[Path],
		outfile: Path
	) -> list[str]:
		
		str_objects = [str(obj) for obj in objects]
		str_libs = [str(lib) for lib in libraries]

		if outfile.exists():
			outfile.unlink()

		# /LD builds a DLL
		cmd = [binary, "/nologo", "/LD", f"/Fe{str(outfile)}", *str_objects, *str_libs]
		return cmd


	def buildExecutable(
		self,
		binary: str,
		objects: list[Path],
		libraries: list[Path],
		outfile: Path
	) -> list[str]:
		
		str_objects = [str(obj) for obj in objects]
		str_libs = [str(lib) for lib in libraries]

		if outfile.exists():
			outfile.unlink()

		cmd = [binary, "/nologo", f"/Fe{str(outfile)}", *str_objects, *str_libs]
		return cmd
