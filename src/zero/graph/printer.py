from .nodes import *
from .visitor import NodeVisitor
from zero.reporter.get import getReporter

class NodePrinter(NodeVisitor):


	def __init__(self) -> None:
		super().__init__()
		self._depth: int = 0
		self._visited_ids: set[int] = set()
		self._reporter = getReporter()

		self._color_map = {
			0: "bold red",
			1: "bold yellow",
			2: "bold blue",
			3: "bold green",
			4: "bold magenta"
		}


	def _get_indent(self) -> str:
		return "   " * self._depth


	def _print_node_base(self, node: Node, label: str, details: str) -> bool:

		indent = self._get_indent()

		color = self._color_map[self._depth % len(self._color_map)]

		self._reporter.print(f"{indent}[{color}]({label})[/{color}] {details}")

		if id(node) in self._visited_ids:
			return True
			
		self._visited_ids.add(id(node))
		return False


	def visitRootNode(self, node: RootNode):
		if self._print_node_base(node, "Root", f"{len(node.targets)} targets"):
			return
			
		self._depth += 1
		for target in node.targets:
			self.visit(target)
		self._depth -= 1


	def visitExecutableNode(self, node: ExecutableNode):
		if self._print_node_base(node, "Executable", str(node.targetpath.name)):
			return
			
		self._depth += 1
		for src in node.sources:
			self.visit(src)
		for lib in node.linked_libraries:
			self.visit(lib)
		self._depth -= 1


	def visitStaticLibraryNode(self, node: StaticLibraryNode):
		if self._print_node_base(node, "StaticLibrary", str(node.libpath.name)):
			return
			
		self._depth += 1
		for src in node.sources:
			self.visit(src)
		for lib in node.linked_libraries:
			self.visit(lib)
		self._depth -= 1


	def visitSharedLibraryNode(self, node: SharedLibraryNode):
		if self._print_node_base(node, "SharedLibrary", str(node.libpath.name)):
			return
			
		self._depth += 1
		for src in node.sources:
			self.visit(src)
		for lib in node.linked_libraries:
			self.visit(lib)
		self._depth -= 1
		

	def visitPreCompiledLibraryNode(self, node: PreCompiledLibraryNode):
		if self._print_node_base(node, "PreCompiledLibrary", str(node.libpath)):
			return
	

	def visitSourceNode(self, node: SourceNode):
		details = f"{node.filepath}"
		if self._print_node_base(node, "Source", details):
			return
			
		self._depth += 1
		for header in node.deps:
			self.visit(header)
		self._depth -= 1


	def visitHeaderNode(self, node: HeaderNode):
		if self._print_node_base(node, "Header", str(node.filepath)):
			return
			
		self._depth += 1
		for header in node.deps:
			self.visit(header)
		self._depth -= 1