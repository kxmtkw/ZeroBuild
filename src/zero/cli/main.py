from zero.orchestrator import Orchestrator
from zero.cli.args import setupParser, parseArguments


def runCli(orchestrator: Orchestrator):

	parser = setupParser()
	args = parseArguments(parser)


	if args.command == "make":
		if len(args.target) == 0:
			orchestrator.makeBuild(fresh=args.fresh)
		else:
			orchestrator.makeTargets(args.target, fresh=args.fresh)

	elif args.command == "run":
		orchestrator.runExecutable(args.executable, args.executable_args, fresh=args.fresh)
		

def main():
	orchestrator = Orchestrator()
	try:
		runCli(orchestrator)
	except KeyboardInterrupt:
		orchestrator.abort()
		exit()
