from pathlib import Path

from zero.errors.errors import ZeroAPIError, ZeroError, ZeroCompilationError
from zero.graph.printer import NodePrinter
from zero.interface.build import Build
from zero.graph.constructor import GraphConstructor
from zero.builder.builder import Builder
from zero.compilers.get import getCompiler

from zero.analyzers.cycle_detector import CycleDetector
from zero.analyzers.stale_detector import StaleDetector

from zero.interface.executable import Executable
from zero.interface.target import Target
from zero.orchestrator.config import BuildConfig, Directory
from zero.orchestrator.executor import Executor
from zero.reporter import TerminalReporter

from zero.utils import ModuleLoader


class Orchestrator:

	def __init__(self) -> None:
		self.reporter = TerminalReporter()
		self.config_file = Path("zerobuild.py")
		self.builder: Builder | None = None


	def loadConfigFile(self) -> ModuleLoader:

		if not self.config_file.exists():
			raise ZeroError(f"Config file '{str(self.config_file)}' not found.")
		
		try:
			module = ModuleLoader(self.config_file)
		except ZeroAPIError as e:
			self.reportAndExit(str(e))
		except Exception as e:
			self.reportAndExit(f"[{e.__class__.__name__}] {str(e)}")

		
		return module
	

	def configureBuild(self, build_dir: Path, fresh_build: bool, threads: int) -> BuildConfig:

		config = BuildConfig()
		config.directory = Directory()
		
		config.directory.build = build_dir
		config.directory.binary = build_dir / "bin"
		config.directory.objects = build_dir / "objects"
		config.directory.lib = build_dir / "lib"
		config.directory.shared_lib = config.directory.lib / "shared"
		config.directory.static_lib = config.directory.lib / "static"

		config.directory.create_all()

		config.fresh_build = fresh_build

		config.threads = threads

		return config


	def make(
		self,
		*,
		specific_targets: list[str] = [],
		fresh_build: bool = False,
		threads: int = 1
		):

		module = self.loadConfigFile()
		build = self.getBuild(module)
		targets = self.getTargets(module)

		needed_targets = []

		# getting all targets
		for target in targets:
			# if specific targets is empty, we default to all targets.
			if len(specific_targets) == 0:
				break

			if target._name in specific_targets:
				specific_targets.remove(target._name)
				needed_targets.append(target)

		# exit if we do not find all specied targets
		if len(specific_targets) > 0:
			self.reportAndExit(f"Target{'s' if len(specific_targets) > 1 else ''} not found: {', '.join(specific_targets)}")
				
		
		self.reporter.startPhase("Configuration", "Configuring")

		config = self.configureBuild(build.directory, fresh_build, threads)
			
		self.reporter.taskDone("Directory", f"{str(build.directory)} chosen.")
		self.reporter.taskDone("Threads", f"compiling with {config.threads} threads")


		# Making the DAG
		self.graph = GraphConstructor(config)

		
		try:
			root = self.graph.makeRoot(build, targets, needed_targets)
		except ZeroError as e:
			self.reportAndExit(str(e))
			
		self.reporter.taskDone("Graph", "constructed")

		# Detecting any cycles
		cycle = CycleDetector()
		
		try:
			cycle.visit(root)
		except ZeroError as e:
			self.reportAndExit(str(e))

		self.reporter.taskDone("Cycles", "none detected")

		if config.fresh_build:
			msg = "skipped - fresh make"
		else:
			stale = StaleDetector(config)
			stale.visit(root)
			count = stale.getStaleCount()
			msg = "no need for compilation" if count == 0 else f"detected (count = {count})"
			
		self.reporter.taskDone("Staleness", msg)		
		self.reporter.endPhase("Configuration complete.")	


		try:
			self.builder = Builder(config)
		except ZeroCompilationError as e:
			self.reportAndExit(str(e))

		self.builder.visit(root)


	def getBuild(self, module: ModuleLoader) -> Build:
	
		build = module.getAttribute("build")

		if not isinstance(build, Build):
			self.reportAndExit(f"Attribute 'build' not found or is not an instance of Build.")
		
		if build._compiler is None:
			self.reportAndExit(f"No compiler provided for build.")

		try:
			build._compiler_object = getCompiler(build._compiler)
		except ValueError:
			self.reportAndExit(f"Unknown compiler: {build._compiler}")
		
		return build


	def getTargets(self, module: ModuleLoader) -> list[Target]:

		build = self.getBuild(module)

		targets: list[Target] = []

		for name, value in module:

			if not isinstance(value, Target):
				continue

			if not hasattr(value, "_name"):
				value._name = name

			try:
				value._compiler_object = build._compiler_object if value._compiler == "inherit" else getCompiler(value._compiler)
			except ValueError:
				self.reportAndExit(f"Unknown compiler: {value._compiler}")
			
			targets.append(value)


		return targets


	def runExecutable(self, name: str, args: list[str], *, fresh_build: bool = False):
		
		module = self.loadConfigFile()
		build = self.getBuild(module)
		targets = self.getTargets(module)

		executable: Executable | None = None

		for target in targets:
			if isinstance(target, Executable) and target.name == name:
				executable = target
				break

		if executable is None:
			self.reportAndExit(f"Executable {name} not found.")

		# mock config to get the binary dir
		config = self.configureBuild(build.directory, False, 1)
		executable_path = config.directory.binary / name

		if not executable_path.exists() or fresh_build:
			self.make(specific_targets=[executable._name], fresh_build=fresh_build)
		
		executor = Executor(str(executable_path), args)

		executor.run()


	def abort(self):
		if self.builder: 
			self.builder.halt()
			
		self.reporter.endPhase("User Aborted")


	def reportAndExit(self, error: str):
		self.reporter.error(str(error))
		exit(1)




