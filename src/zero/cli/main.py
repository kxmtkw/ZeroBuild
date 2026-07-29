from zero.orchestrator import Orchestrator
from zero.cli.args import setupParser, parseArguments


def runCli(orchestrator: Orchestrator):

	parser = setupParser()
	args = parseArguments(parser)


	if args.command == "make":
		orchestrator.make(specific_targets=args.target, fresh_build=args.fresh, threads=args.threads)

	elif args.command == "run":
		orchestrator.runExecutable(args.executable, args.executable_args, fresh_build=args.fresh)
		

def main():
	orchestrator = Orchestrator()
	try:
		runCli(orchestrator)
	except KeyboardInterrupt:
		orchestrator.abort()
		exit()
