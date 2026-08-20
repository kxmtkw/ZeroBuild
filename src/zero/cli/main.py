from zero.orchestrator import Orchestrator
from zero.cli.args import setupParser, parseArguments


def runCli(orchestrator: Orchestrator):

	parser = setupParser()
	args = parseArguments(parser)


	if args.command == "make":
		orchestrator.setUserOptions(args.user)
		orchestrator.make(specific_targets=args.targets, fresh_build=args.fresh, threads=args.threads)

	elif args.command == "run":
		orchestrator.runExecutable(args.executable, args.executable_args, fresh_build=args.fresh)

	elif args.command == "clean":
		orchestrator.clean()

	elif args.command == "graph":
		orchestrator.printGraph()

	elif args.command == "version":
		from zero import __version__
		print(__version__)


def main():
	orchestrator = Orchestrator()
	try:
		runCli(orchestrator)
	except KeyboardInterrupt:
		orchestrator.abort()
		exit()
