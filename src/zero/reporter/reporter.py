from rich.console import Console
from rich.status import Status


class TerminalReporter:
	"""
	Class for reporting build phases and logs to the terminal.
	"""

	_instance: TerminalReporter | None = None


	def __init__(self) -> None:
		self._console = Console()
		self._status: Status | None = None

		self._is_phase: bool = False
		self._phase_name: str = ""
		self._phase_action: str = ""

		if TerminalReporter._instance is None:
			TerminalReporter._instance = self


	def startPhase(self, phase_name: str, phase_action: str):

		if self._is_phase:
			self.endPhase("Interrupted")

		self._phase_name = phase_name
		self._phase_action = phase_action
		self._is_phase = True
		self._console.print(f"[bold blue]── {self._phase_name}")
		self._status = self._console.status(f"[bold blue]{self._phase_action}", spinner="dots")
		self._status.start()


	def endPhase(self, msg: str):

		if not self._is_phase:
			return
		
		if self._status:
			self._status.stop()
		self._console.print(f"    [blue]└─ {msg}\n")

		self._is_phase = False

	
	def taskDone(self, task: str, msg: str):
		if self._is_phase:
			self._console.print(f"    [blue]│[/blue][bold green] {task:<16}[/bold green] {msg} ")
		else:
			self._console.print(f"[bold green] {task:<16}[/bold green] {msg} ")


	def error(self, msg: str):
		self._console.print(f"[bold red]Error: {msg} [/bold red]")
	