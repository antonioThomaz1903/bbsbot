import asyncio
from collections.abc import Awaitable, Callable
from typing import Any


TaskFunction = Callable[[], Awaitable[None]]


class TaskManager:
    def __init__(self):
        self._current_task: asyncio.Task | None = None
        self._current_name: str | None = None

    @property
    def is_running(self) -> bool:
        return (
            self._current_task is not None
            and not self._current_task.done()
        )

    @property
    def current_name(self) -> str | None:
        return self._current_name

    async def start(self, name: str, task_function: TaskFunction):
        if self.is_running:
            raise RuntimeError(
                f"Já existe uma tarefa em execução: {self._current_name}"
            )

        self._current_name = name
        self._current_task = asyncio.create_task(
            self._run(name, task_function)
        )

    async def _run(self, name: str, task_function: TaskFunction):
        try:
            print(f"[TaskManager] Iniciando: {name}")
            await task_function()

        except asyncio.CancelledError:
            print(f"[TaskManager] Cancelada: {name}")
            raise

        except Exception as error:
            print(f"[TaskManager] Erro em {name}: {error}")

        finally:
            self._current_task = None
            self._current_name = None
            print(f"[TaskManager] Finalizada: {name}")

    async def cancel(self):
        if not self.is_running:
            return False

        task = self._current_task
        task.cancel()

        try:
            await task
        except asyncio.CancelledError:
            pass

        return True

    async def wait(self):
        if self._current_task is not None:
            await self._current_task