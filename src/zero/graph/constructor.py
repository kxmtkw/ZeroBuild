from zero.graph.nodes import *
from zero.graph.target_name import TargetNameGenerator

from zero.compilers import BaseCompilerDriver
from zero.compilers.manager import CompilerManager
from zero.compilers.types import CompilerType

from zero.interface.target import Target
from zero.interface.build import Build
from zero.interface.executable import Executable
from zero.interface.source import Source
from zero.interface.library import Library
from zero.interface.static_lib import StaticLibrary
from zero.interface.shared_lib import SharedLibrary
from zero.interface.precomp_lib import PreCompiledLibrary

from zero.orchestrator.config import BuildConfig

from zero.errors.errors import ZeroCompilationError, ZeroHeaderNotFoundError, ZeroSourceNotFoundError
from zero.reporter import getReporter
from zero.utils import CacheManager


class GraphConstructor:
	"""
	Uses interface classes to construct the DAG.
	"""

	def __init__(self, config: BuildConfig) -> None:

		self.visited_headers: dict[Path, HeaderNode] = {}
		self.visited_sources: dict[Path, SourceNode] = {}

		self.made_executables: dict[Executable, ExecutableNode] = {}
		self.made_static_libs: dict[StaticLibrary, StaticLibraryNode] = {}
		self.made_shared_libs: dict[SharedLibrary, SharedLibraryNode] = {}
		self.made_compiled_libs: dict[PreCompiledLibrary, PreCompiledLibraryNode] = {}

		self.build_dir = config.directory.build
		self.object_dir = config.directory.objects
		self.exec_dir = config.directory.binary
		self.static_lib_dir = config.directory.static_lib
		self.shared_lib_dir = config.directory.shared_lib

		self.target_name_gen = TargetNameGenerator()

		self.cache: CacheManager = CacheManager(self.build_dir / "deps.cache")
		self.old_mtime_cache = CacheManager(self.build_dir / "old_mtime.cache")
		self.mtime_cache = CacheManager(self.build_dir / "mtime.cache")

		# causes a rebuild of the DAG if the build file updated
		if config.build_script_updated:
			self.old_mtime_cache.clear()
				

	def makeRoot(self, build: Build, all_targets: list[Target], specific_targets: list[Target] = []) -> RootNode:

		targets = []
		compilers = {}

		# all targets are built one by one irrespective of location in the dag

		for t in all_targets:

			# the compiler switching logic might fail if a library dependency uses a different compiler
			# but this would be fine because dependencies will always be defined first due to python syntax
			# so the library node would already be created

			self.current_compiler = t._compiler_object
			node = self.makeTargetNode(t)
			compilers[node] = self.current_compiler

			if len(specific_targets) == 0 or t in specific_targets:
				targets.append(node)

		root = RootNode(
			targets,
			compilers
		)

		self.cache.save()
		self.mtime_cache.save()
		
		return root
	

	def makeTargetNode(self, target) -> TargetNode:

		if isinstance(target, Executable):
			return self.makeExecutableNode(target)
		elif isinstance(target, StaticLibrary):
			return self.makeStaticLibraryNode(target)
		elif isinstance(target, SharedLibrary):
			return self.makeSharedLibraryNode(target)
		else:
			raise RuntimeError()


	def makeLibraryNode(self, lib: Library) -> LibraryNode:

		if isinstance(lib, PreCompiledLibrary):
			return self.makePrecompiledLibNode(lib)
		elif isinstance(lib, StaticLibrary):
			return self.makeStaticLibraryNode(lib)
		elif isinstance(lib, SharedLibrary):
			return self.makeSharedLibraryNode(lib)
		else:
			raise RuntimeError()


	def makeExecutableNode(self, exe: Executable) -> ExecutableNode:
		
		if exe in self.made_executables:
			return self.made_executables[exe]
		
		outfile = self.target_name_gen.executable(self.exec_dir, exe._name)
		
		include_dirs: list[Path] = []
		lib_nodes: list[LibraryNode] = []

		for lib in exe._linked_libs:
			lib_node = self.makeLibraryNode(lib)
			lib_nodes.append(lib_node)
			include_dirs.extend(lib_node.public_headers)        
		
		include_dirs.extend(exe.headers.private)

		source_nodes = self.makeSourceNodes(exe.source, include_dirs)

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
		
		outfile = self.target_name_gen.staticLib(self.static_lib_dir, lib._name)
		
		include_dirs: list[Path] = []
		lib_nodes: list[LibraryNode] = []

		for sub_lib in lib._linked_libs:
			lib_node = self.makeLibraryNode(sub_lib)
			lib_nodes.append(lib_node)
			include_dirs.extend(lib_node.public_headers)        
		
		include_dirs.extend(lib.headers.private)
		include_dirs.extend(lib.headers.public)

		source_nodes = self.makeSourceNodes(lib.source, include_dirs)
		
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
		
		targetpath, libpath = self.target_name_gen.sharedLib(self.static_lib_dir, lib._name)

		include_dirs: list[Path] = []
		lib_nodes: list[LibraryNode] = []

		for sub_lib in lib._linked_libs:
			lib_node = self.makeLibraryNode(sub_lib)
			lib_nodes.append(lib_node)
			include_dirs.extend(lib_node.public_headers)        
		
		include_dirs.extend(lib.headers.private)
		include_dirs.extend(lib.headers.public)

		source_nodes = self.makeSourceNodes(lib.source, include_dirs)
		
		node = SharedLibraryNode(
			targetpath,
			libpath,
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


	def makeHeaderNode(self, path: Path, include_dirs: list[Path]) -> HeaderNode:

		if path in self.visited_headers:
			return self.visited_headers[path]

		if not path.exists():
			raise ZeroHeaderNotFoundError(f"Header file '{str(path)}' not found")
		
		header = HeaderNode(
			path,
			[]
		)

		self.visited_headers[path] = header

		# 0 because if the old mtime cache does not exist, new_mtime will always be greater than 0
		old_mtime = self.old_mtime_cache.get(str(path), default=0, valid_classes=(float,int,)) 
		new_mtime = self.mtime_cache.set(str(path), value=path.stat().st_mtime)


		if new_mtime > old_mtime:
			cached_deps = None
		else:
			cached_deps = self.cache.get(str(path), default=None, valid_classes=(list,))

		if cached_deps is None:
			deps = self.current_compiler.getDependencies(path, include_dirs=include_dirs) 
			self.cache.set(str(path), value=[str(d) for d in deps])
		else:
			deps = [Path(d) for d in cached_deps]

		try:
			included_headers = [self.makeHeaderNode(d, include_dirs) for d in deps]
		except ZeroHeaderNotFoundError as e:
			raise ZeroHeaderNotFoundError(str(e) + f"\n -- while processing header file '{str(path)}'")
		
		header.deps = included_headers
		
		return header
			

	def _makeSourceNode(self, path: Path, include_dirs: list[Path]) -> SourceNode:

		if path in self.visited_sources:
			return self.visited_sources[path]

		if not path.exists():
			# this almost will never be raised because the interface object Source will check, but just in case
			raise ZeroSourceNotFoundError(f"Source file '{str(path)}' not found")
		
		outfile = self.target_name_gen.objectFile(self.object_dir / path.parent, path.name)

		if not outfile.parent.exists():
			outfile.parent.mkdir(511, True, True)

		source = SourceNode(
			path,
			outfile,
			[]
		)
		self.visited_sources[path] = source

		# old mtime defaults to 0, so it always rebuilds if old mtime is missing

		old_mtime = self.old_mtime_cache.get(str(path), default=0, valid_classes=(float,int,)) 
		new_mtime = self.mtime_cache.set(str(path), value=path.stat().st_mtime)


		if new_mtime > old_mtime:
			cached_deps = None
		else:
			cached_deps = self.cache.get(str(path), default=None, valid_classes=(list,))

		# get deps if the cache is missing or file updated

		if cached_deps is None:
			try:
				deps = self.current_compiler.getDependencies(path, include_dirs=include_dirs) 
			except ZeroCompilationError as e:
				raise ZeroHeaderNotFoundError(e.error + f"\n -- while processing source file '{str(path)}'")
			
			self.cache.set(str(path), value=[str(d) for d in deps])
		else:
			deps = [Path(d) for d in cached_deps]

		try:
			included_headers = [self.makeHeaderNode(d, include_dirs) for d in deps]
		except ZeroHeaderNotFoundError as e:
			raise ZeroHeaderNotFoundError(str(e) + f"\n -- while processing source file '{str(path)}'")

		source.deps = included_headers

		return source
	

	def makeSourceNodes(self, source: Source, include_dirs: list[Path]) -> list[SourceNode]:
		return [self._makeSourceNode(p, include_dirs) for p in source._sources_paths]