from pathlib import Path


class GccCommandGenerator:
	"""
	Helper class to generate commands for gcc (and similar compilers).
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
		include_args = [f"-I{str(dir)}" for dir in include_dirs]
		cmd = [binary, "-MM", *include_args, str(filepath)]
		return cmd


	def buildFile(
			self, 
			binary: str,  
			filepath: Path, 
			outfile: Path, 
			*, 
			for_shared = False, 
			include_dirs: list[Path] = [], 
			arguments: list[str] = []
		) -> list[str]:  

		include_args = [f"-I{str(dir)}" for dir in include_dirs]
		cmd = [binary, *arguments, "-c", *include_args, str(filepath), "-o", str(outfile)] 

		if for_shared:
			cmd.append("-fPIC")

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

		cmd = ["ar", "rcs", str(outfile), *str_objects]

		return cmd
		

	def buildSharedLib(
			self, 
			binary: str,  
			objects: list[Path], 
			libraries: list[Path], 
			outfile: Path
		) -> list[str]:  
		
		str_objects = [str(obj) for obj in objects]

		if outfile.exists():
			outfile.unlink()

		cmd = [binary, "-shared", "-o", str(outfile), *str_objects]

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

		cmd = [binary, *str_objects, *str_libs, "-o", str(outfile)]

		return cmd