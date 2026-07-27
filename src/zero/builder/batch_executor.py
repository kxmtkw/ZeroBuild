from concurrent.futures import ThreadPoolExecutor, Future
from typing import Any, Callable


class BatchExecutor:

	def __init__(self, max_workers=3) -> None:
		self._max_workers = max_workers
		self._executor: ThreadPoolExecutor | None = None
		self._futures: list[Future] = []


	def new(self) -> ThreadPoolExecutor:
		return ThreadPoolExecutor(self._max_workers)


	def run(self, func: Callable, *args: Any):

		if not self._executor:
			self._executor = self.new()
		
		future = self._executor.submit(func, *args)
		self._futures.append(future)


	def wait(self) -> list[Future]:

		if not self._executor:
			return []

		self._executor.shutdown()
		futures = self._futures
		self._futures = []

		self._executor = None

		return futures


	def halt(self):

		if not self._executor:
			return

		self._executor.shutdown(False, cancel_futures=True)