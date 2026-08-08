from pathlib import Path
from abc import ABC, abstractmethod
from typing import Sequence

from zero.compilers.base import BaseCompilerDriver

class Node(ABC):
	"""
	Base node class.
	"""
	@abstractmethod
	def __init__(self, **kwargs):
		pass

	def __str__(self) -> str:
		return super().__str__()


class TargetNode(Node):
	"""
	Base target node class.
	A target is something that needs to be compiled by the system.
	A target requires an outfile (path to where the final product is written),
	a list of source nodes and a list of libraries linked against that target.
	"""
	@abstractmethod
	def __init__(self, *, targetpath: Path, sources: Sequence[SourceNode], libs: Sequence[LibraryNode], arguments: list[str], **kwargs):
		super().__init__(**kwargs)
		self.targetpath: Path = targetpath
		self.sources: Sequence[SourceNode] = sources
		self.linked_libraries: Sequence[LibraryNode] = libs
		self.arguments: list[str] = arguments


class LibraryNode(Node):
	"""
	Base library node class.
	A library requires a list of private and public headers. It also requires a filepath pointing to the library's code.
	"""
	@abstractmethod
	def __init__(self, *, libpath: Path, private_headers: Sequence[Path], public_headers: Sequence[Path], **kwargs):
		super().__init__(**kwargs)
		self.libpath: Path = libpath
		self.private_headers: Sequence[Path] = private_headers
		self.public_headers: Sequence[Path] = public_headers


class FileNode(Node):
	"""
	Base file class.
	Represents a file.
	"""
	@abstractmethod
	def __init__(self, *, filepath: Path, **kwargs):
		super().__init__(**kwargs)
		self.filepath: Path = filepath


# Main Nodes


class RootNode(Node):

	def __init__(self, targets: Sequence[TargetNode], compilers: dict[TargetNode, BaseCompilerDriver]):
		super().__init__()
		self.targets: Sequence[TargetNode] = targets
		self.target_compilers: dict[TargetNode, BaseCompilerDriver] = compilers

	def __str__(self) -> str:
		return f"Root()"

	def __repr__(self) -> str:
		return str("root")


class ExecutableNode(TargetNode):

	def __init__(self, exepath: Path, sources: Sequence[SourceNode], libs: Sequence[LibraryNode], arguments: list[str], private_headers: Sequence[Path]):
		super().__init__(targetpath=exepath, sources=sources, libs=libs, arguments=arguments)
		self.private_headers = private_headers

	def __str__(self) -> str:
		return f"Executable({self.targetpath.name})"

	def __repr__(self) -> str:
		return str(self.targetpath.name)


class StaticLibraryNode(TargetNode, LibraryNode):

	def __init__(self, libpath: Path, sources: Sequence[SourceNode], libs: Sequence[LibraryNode], arguments: list[str], private_headers: Sequence[Path], public_headers: Sequence[Path]):
		super().__init__(
			targetpath=libpath, 
			sources=sources,
			libs=libs,
			arguments=arguments,
			libpath=libpath, 
			private_headers=private_headers, 
			public_headers=public_headers
		)

	def __str__(self) -> str:
		return f"StaticLib({self.targetpath.name})"

	def __repr__(self) -> str:
		return str(self.targetpath.name)


class SharedLibraryNode(TargetNode, LibraryNode):

	def __init__(self, targetpath: Path, libpath: Path, sources: Sequence[SourceNode], libs: Sequence[LibraryNode], arguments: list[str], private_headers: Sequence[Path], public_headers: Sequence[Path]):
		super().__init__(
			targetpath=targetpath, 
			sources=sources,
			libs=libs,
			arguments=arguments,
			libpath=libpath, 
			private_headers=private_headers, 
			public_headers=public_headers
		)

	def __str__(self) -> str:
		return f"SharedLib({self.targetpath.name})"

	def __repr__(self) -> str:
			return str(self.targetpath.name)
	

class PreCompiledLibraryNode(LibraryNode, FileNode):

	def __init__(self, libpath: Path, public_headers: Sequence[Path]):
		super().__init__(
			filepath=libpath, 
			libpath=libpath, 
			private_headers=[], 
			public_headers=public_headers
		)

	def __str__(self) -> str:
		return f"PreCompiledLib({str(self.libpath)})"

	def __repr__(self) -> str:
		return str(self.libpath)


class SourceNode(FileNode):
	
	def __init__(self, filepath: Path, outpath: Path, deps: Sequence[FileNode]):
		super().__init__(filepath=filepath)
		self.deps: Sequence[FileNode] = deps
		self.outpath: Path = outpath

	def __str__(self) -> str:
		return f"SourceFile({str(self.filepath)})"

	def __repr__(self) -> str:
		return str(self.filepath)


class HeaderNode(FileNode):

	def __init__(self, filepath: Path, deps: Sequence[FileNode]):
		super().__init__(filepath=filepath)
		self.deps: Sequence[FileNode] = deps

	def __str__(self) -> str:
		return f"HeaderFile({str(self.filepath)})"

	def __repr__(self) -> str:
		return str(self.filepath)