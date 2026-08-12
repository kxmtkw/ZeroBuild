from zero.graph.nodes import Node
from zero.graph.visitor import NodeVisitor
from zero.graph.nodes import *

from zero.orchestrator.config import BuildConfig
from zero.reporter import getReporter
from zero.utils.cache_manager import CacheManager


def markStale(node: Node):
	setattr(node, "_stale", True)


def isStale(node: Node) -> bool:
	return hasattr(node, "_stale")


class StaleDetector(NodeVisitor):


	def __init__(self, config: BuildConfig) -> None:
		super().__init__()
		self.visited_nodes: set[Node] = set()
		self.current_source_outpath: Path | None = None	
		self.stale_count = 0

		self.old_mtime_cache = CacheManager(config.directory.build / "old_mtime.cache")
		self.mtime_cache = CacheManager(config.directory.build / "mtime.cache")


	def markStale(self, node: Node):
		if not hasattr(node, "_stale"):
			setattr(node, "_stale", True)
			self.stale_count += 1


	def getStaleCount(self) -> int:
		return self.stale_count
		

	def visitRootNode(self, node: RootNode):

		if self.visited(node):
			return
		
		for t in node.targets:
			self.visit(t)

		
	def visitExecutableNode(self, node: ExecutableNode):

		if self.visited(node):
			return

		for lib in node.linked_libraries:
			self.visit(lib)

			if isStale(lib):
				self.markStale(node)

		for src in node.sources:
			self.visit(src)

			if isStale(src):
				self.markStale(node)


	def visitStaticLibraryNode(self, node: StaticLibraryNode):

		if self.visited(node):
			return

		for lib in node.linked_libraries:
			self.visit(lib)

			if isStale(lib):
				self.markStale(node)

		for src in node.sources:
			self.visit(src)

			if isStale(src):
				self.markStale(node)


	def visitSharedLibraryNode(self, node: SharedLibraryNode):
		
		if self.visited(node):
			return

		for lib in node.linked_libraries:
			self.visit(lib)

			if isStale(lib):
				self.markStale(node)

		for src in node.sources:
			self.visit(src)

			if isStale(src):
				self.markStale(node)
	

	def visitPreCompiledLibraryNode(self, node: PreCompiledLibraryNode):
		
		if self.visited(node):
			return


	def visitSourceNode(self, node: SourceNode):

		if self.visited(node):
			return

		old_mtime = self.old_mtime_cache.get(str(node.filepath), default=0, valid_classes=(float,int,)) 
		new_mtime = self.mtime_cache.get(str(node.filepath), default=1, valid_classes=(float,int,)) 

		if new_mtime > old_mtime:
			self.markStale(node)
			return

		self.current_source_outpath = node.filepath
		
		for header in node.deps:
			self.visit(header)

			if isStale(header):
				self.markStale(node)
				return

		self.current_source_outpath = None


	def visitHeaderNode(self, node: HeaderNode):
		
		if self.visited(node):
			return

		if self.current_source_outpath is None:
			raise RuntimeError("Source path should not have been None. Unexpected.")
		
		old_mtime = self.old_mtime_cache.get(str(node.filepath), default=0, valid_classes=(float,int,)) 
		new_mtime = self.mtime_cache.get(str(node.filepath), default=1, valid_classes=(float,int,)) 

		if new_mtime > old_mtime:
			self.markStale(node)
			return
		
		for header in node.deps:
			self.visit(header)

			if isStale(header):
				markStale(node)
				return

