from pathlib import Path
import subprocess
import sys

from zero.reporter.get import getReporter


class Executor:

	def __init__(self, cmd: str, arguments: list[str]) -> None:
		self._process: subprocess.Popen | None = None
		self._cmd: str = cmd
		self._args: list[str] = arguments
		self._reporter = getReporter()


	def run(self):

		sys.stdout.flush()
		sys.stderr.flush()
	
		try:
			self._process = subprocess.Popen(
				[self._cmd, *self._args],
				stdin=sys.stdin,
				stdout=sys.stdout,
				stderr=sys.stderr
			)
			returncode = self._process.wait()

		except KeyboardInterrupt:

			if self._process and self._process.poll() is None:
				try:
					returncode = self._process.wait(timeout=2)
				except subprocess.TimeoutExpired:
					self._process.kill()
					returncode = self._process.wait()
					
			else:
				returncode = 130

		exit(returncode)
		

		