from zero.compilers.get import getCompiler
from zero.compilers.types import CompilerType
from zero.graph.nodes import *
from zero.compilers import BaseCompiler


from zero.interface.build import Build
from zero.interface.executable import Executable
from zero.interface.source import Source
from zero.interface.library import Library
from zero.interface.static_lib import StaticLibrary
from zero.interface.shared_lib import SharedLibrary
from zero.interface.precomp_lib import PreCompiledLibrary

from zero.orchestrator.config import BuildConfig
from zero.reporter import getReporter
from zero.utils.cache_manager import CacheManager


class GraphConstructor:

	def __init__(self, config: BuildConfig) -> None:

		self.visited_headers: dict[Path, HeaderNode] = {}
		self.visited_sources: dict[Path, SourceNode] = {}

		self.made_executables: dict[Executable, ExecutableNode] = {}
		self.made_static_libs: dict[StaticLibrary, StaticLibraryNode] = {}
		self.made_shared_libs: dict[SharedLibrary, SharedLibraryNode] = {}
		self.made_ompiled_libs: dict[PreCompiledLibrary, PreCompiledLibraryNode] = {}

		self.build_dir = config.directory.build
		self.object_dir = config.directory.objects
		self.exec_dir = config.directory.binary
		self.static_lib_dir = config.directory.static_lib
		self.shared_lib_dir = config.directory.shared_lib

		self.cache: CacheManager = CacheManager(self.build_dir / "deps.cache")
		
		
		self.include_dirs: list[Path] = []
		

	def makeRoot(self, build: Build) -> RootNode:

		targets = []
		compilers = {}

		self.cache.load()

		for t in build._targets:
			self.current_compiler = t._compiler_object
			node = self.makeTargetNode(t)
			targets.append(node)
			compilers[node] = self.current_compiler

		root = RootNode(
			targets,
			compilers
		)

		self.cache.save()
		
		return root
	

	def makeTargetNode(self, target) -> TargetNode:

		if isinstance(target, Executable):
			return self.makeExecutableNode(target)
		elif isinstance(target, StaticLibrary):
			return self.makeStaticLibraryNode(target)
		elif isinstance(target, SharedLibrary):
			return self.makeSharedLibraryNode(target)
		else:
			raise RuntimeError("What")


	def makeLibraryNode(self, lib: Library) -> LibraryNode:

		if isinstance(lib, PreCompiledLibrary):
			return self.makePrecompiledLibNode(lib)
		elif isinstance(lib, StaticLibrary):
			return self.makeStaticLibraryNode(lib)
		elif isinstance(lib, SharedLibrary):
			return self.makeSharedLibraryNode(lib)
		else:
			raise RuntimeError("What")


	def makeExecutableNode(self, exe: Executable) -> ExecutableNode:
		
		if exe in self.made_executables:
			return self.made_executables[exe]
		
		outfile = self.exec_dir / exe._name
		
		include_dirs: list[Path] = []
		lib_nodes: list[LibraryNode] = []

		for lib in exe._linked_libs:
			lib_node = self.makeLibraryNode(lib)
			lib_nodes.append(lib_node)
			include_dirs.extend(lib_node.public_headers)        
		
		include_dirs.extend(exe.headers.private)

		self.include_dirs = include_dirs

		source_nodes = self.makeSourceNodes(exe.source)

		node = ExecutableNode(
			outfile,
			source_nodes,
			lib_nodes,
			exe._arguments,
			exe.headers.private
		)

		self.made_executables[exe] = node

		return node
	


	def makeStaticLibraryNode(self, lib: StaticLibrary) -> StaticLibraryNode:
		
		if lib in self.made_static_libs:
			return self.made_static_libs[lib]
		
		outfile = self.static_lib_dir / ("lib" + lib._name + ".a")

		
		include_dirs: list[Path] = []
		lib_nodes: list[LibraryNode] = []

		for sub_lib in lib._linked_libs:
			lib_node = self.makeLibraryNode(sub_lib)
			lib_nodes.append(lib_node)
			include_dirs.extend(lib_node.public_headers)        
		
		include_dirs.extend(lib.headers.private)
		include_dirs.extend(lib.headers.public)

		self.include_dirs = include_dirs

		source_nodes = self.makeSourceNodes(lib.source)
		
		node = StaticLibraryNode(
			outfile,
			source_nodes,
			lib_nodes,
			lib._arguments,
			lib.headers.private,
			lib.headers.public
		)

		self.made_static_libs[lib] = node
		
		return node
	

	def makeSharedLibraryNode(self, lib: SharedLibrary) -> SharedLibraryNode:

		if lib in self.made_shared_libs:
			return self.made_shared_libs[lib]
		
		outfile = self.shared_lib_dir / ("lib" + lib._name + ".so")

		include_dirs: list[Path] = []
		lib_nodes: list[LibraryNode] = []

		for sub_lib in lib._linked_libs:
			lib_node = self.makeLibraryNode(sub_lib)
			lib_nodes.append(lib_node)
			include_dirs.extend(lib_node.public_headers)        
		
		include_dirs.extend(lib.headers.private)
		include_dirs.extend(lib.headers.public)

		self.include_dirs = include_dirs

		source_nodes = self.makeSourceNodes(lib.source)
		
		node = SharedLibraryNode(
			outfile,
			source_nodes,
			lib_nodes,
			lib._arguments,
			lib.headers.private,
			lib.headers.public
		)

		self.made_shared_libs[lib] = node
		
		return node


	def makePrecompiledLibNode(self, lib: PreCompiledLibrary) -> PreCompiledLibraryNode:
		return PreCompiledLibraryNode(
			lib.filepath,
			lib.headers.public
		)


	def makeHeaderNode(self, path: Path) -> HeaderNode:

		if path in self.visited_headers:
			return self.visited_headers[path]
		
		header = HeaderNode(
			path,
			[]
		)
		self.visited_headers[path] = header

		cached_deps = self.cache.get(str(path), default=None, valid_classes=(list,))

		if cached_deps is None:
			deps = self.current_compiler.getDependencies(path, include_dirs=self.include_dirs) 
			self.cache.set(str(path), value=[str(d) for d in deps])
		else:
			deps = [Path(d) for d in cached_deps]

		included_headers = [self.makeHeaderNode(d) for d in deps]

		header.deps = included_headers
		
		return header
			

	def _makeSourceNode(self, path: Path) -> SourceNode:

		if path in self.visited_sources:
			return self.visited_sources[path]
		
		outfile = self.object_dir / path.parent / (path.name + ".o")

		if not outfile.parent.exists():
			outfile.parent.mkdir(511, True, True)

		source = SourceNode(
			path,
			outfile,
			[]
		)

		self.visited_sources[path] = source

		cached_deps = self.cache.get(str(path), default=None, valid_classes=(list,))
		
		if cached_deps is None:
			deps = self.current_compiler.getDependencies(path, include_dirs=self.include_dirs) 
			self.cache.set(str(path), value=[str(d) for d in deps])
		else:
			deps = [Path(d) for d in cached_deps]
			
		included_headers = [self.makeHeaderNode(d) for d in deps]

		source.deps = included_headers

		return source
	

	def makeSourceNodes(self, source: Source) -> list[SourceNode]:
		return [self._makeSourceNode(p) for p in source._sources_paths]