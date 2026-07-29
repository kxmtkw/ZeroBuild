from rich.console import Console
from rich.status import Status
from rich.panel import Panel

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


	def print(self, *objects, end="\n"):
		self._console.print(*objects, end=end)
		

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

	
	def info(self, title: str, msg: str, color: str = "bold green"):
		if self._is_phase:
			self._console.print(f"    [blue]│[/blue] [{color}]{title:<16}[/{color}] {msg} ")
		else:
			self._console.print(f"[{color}]{title:<16}[/{color}] {msg} ")


	def error(self, msg: str):

		if self._is_phase:
			self.endPhase("Failed")

		self._console.print(Panel(msg, title="Error"))


	def box(self, msg: str, *, title: str | None = None, color: str = ""):

		if self._is_phase:
			self._console.print(f"    [blue]│[/blue]")

		self._console.print(Panel(f"[{color}]{msg.strip()}[/{color}]", title=title, border_style=color, padding=(1,2), expand=False))

		if self._is_phase:
			self._console.print(f"    [blue]│[/blue]")