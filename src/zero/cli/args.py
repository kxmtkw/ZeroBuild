import argparse
import sys


def add_make_command(subparsers: argparse._SubParsersAction) -> None:
	make_parser = subparsers.add_parser(
		"make",
		help="Make the whole build or specific targets",
	)
	make_parser.add_argument(
		"--fresh",
		action="store_true",
		help="Force a clean rebuild.",
	)
	make_parser.add_argument(
		"--threads",
		type=int,
		default=1,
		metavar="COUNT",
		help="Number of threads to use",
	)
	make_parser.add_argument(
		"target",
		nargs="*",
		default=[],
		help="Target/s to build. If none specified, builds all.",
	)


def add_run_command(subparsers: argparse._SubParsersAction) -> None:
	run_parser = subparsers.add_parser(
		"run",
		help="Run executables.",
	)
	run_parser.add_argument(
		"--fresh",
		action="store_true",
		help="Force a clean rebuild before running.",
	)
	run_parser.add_argument(
		"executable",
		help="Name of the executable.",
	)
	run_parser.add_argument(
		"executable_args",
		nargs=argparse.REMAINDER,
		help="Arguments passed directly to the executable",
	)


def setupParser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(prog="zero", description="Zero build system")
	subparsers = parser.add_subparsers(dest="command", required=True)

	add_make_command(subparsers)
	add_run_command(subparsers)

	return parser


def parseArguments(
	parser: argparse.ArgumentParser, args: list[str] | None = None
) -> argparse.Namespace:
	if args is None:
		args = sys.argv[1:]

	return parser.parse_args(args)