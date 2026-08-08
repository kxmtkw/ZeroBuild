import traceback
import shutil

from pathlib import Path

from zero.errors import ZeroAPIError, ZeroCircularDependencyError, ZeroError, ZeroCompilationError
from zero.errors.errors import ZeroHeaderNotFoundError, ZeroSourceNotFoundError
from zero.graph.printer import NodePrinter
from zero.interface.build import Build
from zero.graph.constructor import GraphConstructor
from zero.builder.builder import Builder

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
			self.reportAndExit("Misconfigured Build File", f"Config file '{str(self.config_file)}' not found.")
		
		try:
			module = ModuleLoader(self.config_file)
		except ZeroAPIError as e:
			self.reportAndExit("Misconfigured Build File", str(e))
		except Exception as e:
			self.reportAndExit("Unexpected Error", f"[{e.__class__.__name__}] {str(e)}")
			raise e

		
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

		self.reporter.startPhase("Configuration", "Configuring")

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
			self.reportAndExit("Misconfigured Build File", f"Target{'s' if len(specific_targets) > 1 else ''} not found: {', '.join(specific_targets)}")

		config = self.configureBuild(build.directory, fresh_build, threads)
			
		self.reporter.info("Directory", f"{str(build.directory)} chosen.")
		self.reporter.info("Threads", f"compiling with {config.threads} threads")


		# Making the DAG
		self.graph = GraphConstructor(config)

		
		try:
			root = self.graph.makeRoot(build, targets, needed_targets)
		except (ZeroHeaderNotFoundError, ZeroSourceNotFoundError) as e:
			self.reportAndExit("File Not Found", str(e))
		except Exception as e:
			self.reportError(e)
			
		self.reporter.info("Graph", "constructed")

		# Detecting any cycles
		cycle = CycleDetector()
		
		try:
			cycle.visit(root)
		except ZeroCircularDependencyError as e:
			self.reportAndExit("Circular Dependency Detected", str(e))
		except Exception as e:
			self.reportError(e)

		self.reporter.info("Cycles", "none detected")

		if config.fresh_build:
			msg = "skipped - fresh make"
		else:
			stale = StaleDetector(config)
			stale.visit(root)
			count = stale.getStaleCount()
			msg = "no need for compilation" if count == 0 else f"detected (count = {count})"
			
		self.reporter.info("Staleness", msg)		
		self.reporter.endPhase("Configuration complete.")	


		try:
			self.builder = Builder(config)
		except Exception as e:
			self.reportError(e)

		self.builder.visit(root)


	def getBuild(self, module: ModuleLoader) -> Build:
	
		build = module.getAttribute("build")

		if not isinstance(build, Build):
			self.reportAndExit("Misconfigured Build File", f"Attribute 'build' not found or is not an instance of Build.")
		
		try:
			build._validate()
		except ZeroAPIError as e:
			self.reportAndExit("Misconfigured Build File", str(e))
		
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
				value._validate(build)
			except ZeroAPIError as e:
				self.reportAndExit("Misconfigured Build File", str(e))

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
			self.reportAndExit("Misconfigured Build File", f"Executable {name} not found.")

		# mock config to get the binary dir
		config = self.configureBuild(build.directory, False, 1)
		executable_path = config.directory.binary / name

		if not executable_path.exists() or fresh_build:
			self.make(specific_targets=[executable._name], fresh_build=fresh_build)
		
		executor = Executor(str(executable_path), args)

		executor.run()


	def clearCache(self):
		module = self.loadConfigFile()
		build = self.getBuild(module)

		if build.directory.exists():
			shutil.rmtree(build.directory)
			self.reporter.info("Clearing Cache", f"Cleared {str(build.directory)}")
		else:
			self.reporter.info("Clearing Cache", f"No cache found at {str(build.directory)} - Already Cleared")

		
	def abort(self):
		if self.builder: 
			self.builder.halt()
			
		self.reporter.endPhase("User Aborted")


	def reportError(self, exc: Exception):
		traceback_str = ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__))
		self.reporter.box(traceback_str, title=f"Unexpected {type(exc).__name__}", color="red")
		self.reporter.endPhase("Failed.")
		exit(1)


	def reportAndExit(self, title: str, error: str):
		self.reporter.box(str(error), title=title, color="red")
		self.reporter.endPhase("Failed.")
		exit(1)




