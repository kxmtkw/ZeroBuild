from zero.compilers.get import getCompilerName
from zero.errors.errors import ZeroCompilationError
from zero.graph.nodes import *
from zero.graph.nodes import Node, SharedLibraryNode
from zero.graph.visitor import NodeVisitor

from zero.compilers import BaseCompiler

from zero.orchestrator.config import BuildConfig
from zero.reporter import getReporter
from zero.analyzers.stale_detector import isStale
from zero.utils.cache_manager import CacheManager

from .batch_executor import BatchExecutor

class Builder(NodeVisitor):

	def __init__(self, config: BuildConfig) -> None:

		super().__init__()

		self.batch_executor = BatchExecutor(config.threads)

		self.fresh_build = config.fresh_build

		self.compiling_shared_lib = False

		self.include_dirs: list[Path] = []
		self.visited_nodes: set[object] = set()
		self.current_target_arguments: list[str] = []

		self.reporter = getReporter()

		self.root: RootNode
		self.current_compiler: BaseCompiler
		self.compilers_stack: list[BaseCompiler] = []

		self.old_mtime_cache = CacheManager(config.directory.build / "old_mtime.cache")
		self.mtime_cache = CacheManager(config.directory.build / "mtime.cache")


	def detectStaleness(self, node: Node) -> bool:
		if self.fresh_build:
			return True
		else:
			return isStale(node)


	def visit(self, node: Node):

		if isinstance(node, TargetNode):
			self.compilers_stack.append(self.current_compiler)
			self.current_compiler = self.root.target_compilers[node]

			super().visit(node)

			self.current_compiler = self.compilers_stack.pop()
			return

		super().visit(node)
			

	def visitRootNode(self, node: RootNode):

		self.reporter.startPhase("Compilation", "Compiling")

		self.root = node
		for target in node.targets:
			self.current_compiler = node.target_compilers[target]
			self.visit(target)

		self.old_mtime_cache.save()

		self.reporter.endPhase("Build complete")


	def visitStaticLibraryNode(self, node: StaticLibraryNode):

		if node in self.visited_nodes:
			return
		
		if not self.detectStaleness(node):
			return

		include_dirs = []

		for lib in node.linked_libraries:
			self.visit(lib)
			include_dirs.extend(lib.public_headers)

		include_dirs.extend(node.public_headers)
		include_dirs.extend(node.private_headers)

		self.include_dirs = include_dirs
		
		self.current_target_arguments = node.arguments

		self.compileSources(node.sources)

		self.current_compiler.buildStaticLib([n.outpath for n in node.sources], node.libpath)
		
		self.reporter.taskDone("Link ", f"{node.libpath.name} [bold yellow]via {getCompilerName(self.current_compiler)}[/bold yellow]")

		self.visited_nodes.add(node)


	def visitSharedLibraryNode(self, node: SharedLibraryNode):

		if node in self.visited_nodes:
			return
		
		if not self.detectStaleness(node):
			return

		self.compiling_shared_lib = True

		include_dirs = []

		for lib in node.linked_libraries:
			self.visit(lib)
			include_dirs.extend(lib.public_headers)

		include_dirs.extend(node.public_headers)
		include_dirs.extend(node.private_headers)

		self.include_dirs = include_dirs

		self.current_target_arguments = node.arguments

		self.compileSources(node.sources)

		self.current_compiler.buildSharedLib([n.outpath for n in node.sources], [l.libpath for l in node.linked_libraries], node.libpath)
		
		self.compiling_shared_lib = False

		self.reporter.taskDone("Link ", f"{node.libpath.name} [bold yellow]via {getCompilerName(self.current_compiler)}[/bold yellow]")

		self.visited_nodes.add(node)
	

	def visitPreCompiledLibraryNode(self, node: PreCompiledLibraryNode):

		if not node.libpath.exists():
			raise RuntimeError(f"Could not find pre-compiled library: {node.libpath}")
		
		self.reporter.taskDone("Found", f"{node.libpath}")


	def visitExecutableNode(self, node: ExecutableNode):

		if node in self.visited_nodes:
			return
		
		if not self.detectStaleness(node):
			return
		
		include_dirs = []

		for lib in node.linked_libraries:
			self.visit(lib)
			include_dirs.extend(lib.public_headers)

		include_dirs.extend(node.private_headers)

		self.include_dirs = include_dirs

		self.current_target_arguments = node.arguments

		self.compileSources(node.sources)

		self.current_compiler.buildExecutable([n.outpath for n in node.sources], [n.libpath for n in node.linked_libraries], node.targetpath)

		self.reporter.taskDone("Link ", f"{node.targetpath.name} [bold yellow]via {getCompilerName(self.current_compiler)}[/bold yellow]")

		self.visited_nodes.add(node)

		
	def visitSourceNode(self, node: SourceNode):

		if node in self.visited_nodes:
			return
		
		if not self.detectStaleness(node):
			return

		for deps in node.deps:
			self.visit(deps)

		self.current_compiler.buildFile(
			node.filepath, 
			node.outpath, 
			for_shared=self.compiling_shared_lib, 
			include_dirs=self.include_dirs, 
			arguments=self.current_target_arguments
		)
		self.old_mtime_cache.set(str(node.filepath), value=self.mtime_cache.get(str(node.filepath), default=0, valid_classes=(int,float,)))
		
		self.reporter.taskDone("Built", f"{node.filepath}")

		self.visited_nodes.add(node)
		

	def visitHeaderNode(self, node: HeaderNode):
		for deps in node.deps:
			self.visit(deps)
		self.old_mtime_cache.set(str(node.filepath), value=self.mtime_cache.get(str(node.filepath), default=0, valid_classes=(int,float,)))


	def compileSources(self, sources: Sequence[SourceNode]):

		for source in sources:
			self.batch_executor.run(self.visitSourceNode, source)

		futures = self.batch_executor.wait()

		for future in futures:
			try:
				future.result()
			except Exception as e:
				raise ZeroCompilationError(type(e), str(e))