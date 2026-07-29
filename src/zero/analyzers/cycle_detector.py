from zero.errors import ZeroCircularDependencyError
from zero.graph.nodes import Node
from zero.graph.visitor import NodeVisitor
from zero.graph.nodes import *

from zero.reporter import getReporter


class CycleDetector(NodeVisitor):


	def __init__(self) -> None:
		self.visited_nodes: set[Node] = set()
		self.tracked_nodes: list[Node] = []

		self.cycle: list[Node] = []
		self.is_cycle_detected: bool = False

		self.reporter = getReporter()


	def getCycle(self, node: Node):

		self.is_cycle_detected = True
		
		cycle = []

		for i in range(len(self.tracked_nodes)):
			if self.tracked_nodes[i] == node:
				cycle = self.tracked_nodes[i:]
				cycle.append(node)
				break

		self.cycle = cycle
	

	def visit(self, node: Node):
		
		if self.is_cycle_detected:
			raise ZeroCircularDependencyError(f"{' -> '.join([repr(x) for x in self.cycle])}")
		
		return super().visit(node)
	

	def visitRootNode(self, node: RootNode):

		if node not in self.visited_nodes:
			self.visited_nodes.add(node)

		self.tracked_nodes.append(node)

		for t in node.targets:
			self.visit(t)

		self.tracked_nodes.pop()

		
	def visitExecutableNode(self, node: ExecutableNode):
		if node not in self.visited_nodes:
			self.visited_nodes.add(node)

		if node in self.tracked_nodes:
			self.getCycle(node)
			return

		self.tracked_nodes.append(node)

		for lib in node.linked_libraries:
			self.visit(lib)

		for src in node.sources:
			self.visit(src)

		self.tracked_nodes.pop()


	def visitStaticLibraryNode(self, node: StaticLibraryNode):
		if node not in self.visited_nodes:
			self.visited_nodes.add(node)

		if node in self.tracked_nodes:
			self.getCycle(node)
			return

		self.tracked_nodes.append(node)

		for lib in node.linked_libraries:
			self.visit(lib)

		for src in node.sources:
			self.visit(src)

		self.tracked_nodes.pop()


	def visitSharedLibraryNode(self, node: SharedLibraryNode):
		if node not in self.visited_nodes:
			self.visited_nodes.add(node)

		if node in self.tracked_nodes:
			self.getCycle(node)
			return

		self.tracked_nodes.append(node)

		for lib in node.linked_libraries:
			self.visit(lib)

		for src in node.sources:
			self.visit(src)

		self.tracked_nodes.pop()
	

	def visitPreCompiledLibraryNode(self, node: PreCompiledLibraryNode):
		if node not in self.visited_nodes:
			self.visited_nodes.add(node)


	def visitSourceNode(self, node: SourceNode):
		if node not in self.visited_nodes:
			self.visited_nodes.add(node)

		if node in self.tracked_nodes:
			self.getCycle(node)
			return

		self.tracked_nodes.append(node)

		for header in node.deps:
			self.visit(header)

		self.tracked_nodes.pop()


	def visitHeaderNode(self, node: HeaderNode):
		if node not in self.visited_nodes:
			self.visited_nodes.add(node)

		if node in self.tracked_nodes:
			self.getCycle(node)
			return

		self.tracked_nodes.append(node)

		for header in node.deps:
			self.visit(header)

		self.tracked_nodes.pop()
