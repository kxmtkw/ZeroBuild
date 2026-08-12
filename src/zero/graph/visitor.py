from abc import ABC, abstractmethod
from typing import Callable, Type

from zero.graph.nodes import *


class NodeVisitor(ABC):


	def __init__(self) -> None:
		self._visitor_visited_nodes: set[Node] = set()


	def visit(self, node: Node):

		method_name = f"visit{type(node).__name__}"
		method = getattr(self, method_name)

		if method_name is None:
			raise NotImplementedError(f"{method_name} not implemented for {type(self)}")
		
		method(node)

		self._visitor_visited_nodes.add(node)


	def visited(self, node: Node) -> bool:
		return (node in self._visitor_visited_nodes)


	@abstractmethod
	def visitRootNode(self, node: RootNode) -> None:
		pass 

	@abstractmethod
	def visitExecutableNode(self, node: ExecutableNode) -> None:
		pass

	@abstractmethod
	def visitStaticLibraryNode(self, node: StaticLibraryNode) -> None:
		pass

	@abstractmethod
	def visitSharedLibraryNode(self, node: SharedLibraryNode) -> None:
		pass

	@abstractmethod
	def visitPreCompiledLibraryNode(self, node: PreCompiledLibraryNode) -> None:
		pass
	
	@abstractmethod
	def visitSourceNode(self, node: SourceNode) -> None:
		pass

	@abstractmethod
	def visitHeaderNode(self, node: HeaderNode) -> None:
		pass
