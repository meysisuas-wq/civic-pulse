from typing import Callable, Any, Dict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4, UUID
import asyncio, structlog

logger = structlog.get_logger()

@dataclass
class Task:
    id: UUID = field(default_factory=uuid4)
    name: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    priority: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    max_retries: int = 3
    retry_count: int = 0
    status: str = "pending"

class WorkerQueue:
    def __init__(self, max_workers: int = 5):
        self._queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
        self._handlers: Dict[str, Callable] = {}
        self._max_workers = max_workers
        self._workers: list = []
        self._running = False

    def register_handler(self, task_name: str, handler: Callable):
        self._handlers[task_name] = handler

    async def enqueue(self, task: Task):
        await self._queue.put((-task.priority, task.created_at, task))
        logger.info("task_enqueued", task_id=str(task.id), name=task.name)

    async def _process_task(self, task: Task):
        handler = self._handlers.get(task.name)
        if not handler: return
        task.status = "processing"
        try:
            await handler(task.payload)
            task.status = "completed"
        except Exception as e:
            task.retry_count += 1
            if task.retry_count < task.max_retries:
                task.status = "retrying"
                await self.enqueue(task)
            else:
                task.status = "failed"

    async def _worker(self, worker_id: int):
        while self._running:
            try:
                _, _, task = await asyncio.wait_for(self._queue.get(), timeout=1.0)
                await self._process_task(task)
            except asyncio.TimeoutError:
                continue

    async def start(self):
        self._running = True
        for i in range(self._max_workers):
            self._workers.append(asyncio.create_task(self._worker(i)))

    async def stop(self):
        self._running = False
        await asyncio.gather(*self._workers, return_exceptions=True)
        self._workers.clear()

    @property
    def pending_count(self) -> int:
        return self._queue.qsize()

queue = WorkerQueue()
