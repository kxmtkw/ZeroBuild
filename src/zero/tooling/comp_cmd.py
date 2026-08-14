from typing import Any

import json

from zero.graph.nodes import *
from zero.graph.visitor import NodeVisitor

from zero.orchestrator.config import BuildConfig


class CompileCommandsGenerator(NodeVisitor):
	"""
	Class to generate `compile_commands.json` used by a lot of intellisense providers.
	"""

	def __init__(self, config: BuildConfig) -> None:

		super().__init__()

		self.root_directory = config.build_script.parent.absolute()
		self.compile_commands_json = config.directory.build / "compile_commands.json"

		# really only needs to be rebuilt if project structure changes which only changes
		# if the build script itself updates
		self.needs_rebuilding = config.build_script_updated

		self.compiling_shared_lib = False
		self.active_include_dirs: list[Path] = []
		self.active_target_arguments: list[str] = []	

		self.active_compiler: BaseCompilerDriver
		self.active_compilers_map: dict[TargetNode, BaseCompilerDriver] = {}
		self.active_compilers_stack: list[BaseCompilerDriver] = []

		self.compile_commands_data: list[dict[str, Any]] = []


	def addEntry(self, file: Path, out: Path, cmd: list[str]):
		self.compile_commands_data.append(
			{
				"directory": str(self.root_directory),
				"file": str(file.absolute()),
				"arguments": cmd,
				"output": str(out.absolute())
			}
		)


	def export(self):
		with open(self.compile_commands_json, "w") as file:
			json.dump(self.compile_commands_data, file, indent=4)


	def pushCompiler(self, compiler: BaseCompilerDriver):
		self.active_compilers_stack.append(self.active_compiler)
		self.active_compiler = compiler


	def popCompiler(self):
		self.active_compiler = self.active_compilers_stack.pop()


	def visitRootNode(self, node: RootNode):

		if not self.needs_rebuilding:
			return

		self.active_compilers_map = node.target_compilers

		for target in node.targets:
			self.active_compiler = self.active_compilers_map[target]
			self.visit(target)

		self.export()


	def visitStaticLibraryNode(self, node: StaticLibraryNode):

		if self.visited(node):
			return
		
		include_dirs = []

		for lib in node.linked_libraries:
			self.visit(lib)
			include_dirs.extend(lib.public_headers)

		include_dirs.extend(node.public_headers)
		include_dirs.extend(node.private_headers)

		self.include_dirs = include_dirs
		self.current_target_arguments = node.arguments

		self.pushCompiler(self.active_compilers_map[node])

		for source in node.sources:
			self.visitSourceNode(source)

		self.popCompiler()


	def visitSharedLibraryNode(self, node: SharedLibraryNode):

		if self.visited(node):
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

		self.pushCompiler(self.active_compilers_map[node])

		for source in node.sources:
			self.visitSourceNode(source)

		self.popCompiler()
		self.compiling_shared_lib = False


	def visitExecutableNode(self, node: ExecutableNode):

		if self.visited(node):
			return

		include_dirs = []
		
		for lib in node.linked_libraries:
			self.visit(lib)
			include_dirs.extend(lib.public_headers)

		include_dirs.extend(node.private_headers)

		self.include_dirs = include_dirs
		self.current_target_arguments = node.arguments

		self.pushCompiler(self.active_compilers_map[node])

		for source in node.sources:
			self.visitSourceNode(source)

		self.popCompiler()


	def visitPreCompiledLibraryNode(self, node: PreCompiledLibraryNode):
		pass


	def visitHeaderNode(self, node: HeaderNode) -> None:
		pass

		
	def visitSourceNode(self, node: SourceNode):

		if self.visited(node):
			return

		for deps in node.deps:
			self.visit(deps)

		cmd = self.active_compiler.buildFile(
			node.filepath, 
			node.outpath, 
			for_shared=self.compiling_shared_lib, 
			include_dirs=self.include_dirs, 
			arguments=self.current_target_arguments,
			do_not_compile=True
		)

		self.addEntry(node.filepath, node.outpath, cmd)
