from __future__ import annotations
from typing import Protocol, Iterator, runtime_checkable
from pathlib import Path
import json
import logging

from src.task import Task

logger = logging.getLogger(__name__)


@runtime_checkable
class TaskSource(Protocol):
    """
    Контракт для источников задач

    """
    def get_tasks(self) -> Iterator[Task]:
        ...


class FileTaskSource:
    """
    Источник - JSON-файл

    """
    
    def __init__(self, filepath: str | Path) -> None:
        self.filepath = Path(filepath)
        logger.debug(f"File Task Source initialized: {self.filepath}")
    
    def get_tasks(self) -> Iterator[Task]:
        if not self.filepath.exists():
            logger.warning(f"File is not found {self.filepath}")
            return iter([])
        logger.debug(f"Reading {self.filepath}")
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                yield Task(
                    id=item["id"],
                    payload=item.get("payload", {})
                )
        logger.info(f"Finished reading {len(data)} tasks from {self.filepath}")


class GeneratorTaskSource:
    """
    Источник задач - программная генерация.

    """
    
    def __init__(self, count: int = 5, prefix: str = "gen") -> None:
        self.count = count
        self.prefix = prefix
        logger.debug(f"Generator initialized: count= {count}, prefix= {prefix}")

    def get_tasks(self) -> Iterator[Task]:
        logger.debug("Generating tasks")
        for i in range(self.count):
            yield Task(
                id=f"{self.prefix}_{i}",
                payload={
                    "step": i,
                    "generated": True,
                    "source": "generator"
                }
            )
        logger.info(f"Finished generating {self.count} tasks")

class APIStubTaskSource:
    """
    Заглушка внешнего API-источника задач.

    """

    DEFAULT_TASKS: list[dict] = [
        {"id": "api_1", "payload": {"source": "stub", "priority": "high"}},
        {"id": "api_2", "payload": {"source": "stub", "priority": "low"}},
        {"id": "api_3", "payload": {"source": "stub", "priority": "medium"}},
    ]
    
    def __init__(self, mock_tasks: list[dict] | None = None) -> None:
        self.mock_tasks = mock_tasks or self.DEFAULT_TASKS.copy()
        logger.debug(f"APIStubTaskSource initialized: {len(self.mock_tasks)} tasks")

    def get_tasks(self) -> Iterator[Task]:
        logger.debug("Returning tasks from API stub")
        for item in self.mock_tasks:
            yield Task(
                id=item["id"],
                payload=item.get("payload", {})
            )
    
    def __repr__(self) -> str:
        return f"APIStubTaskSource(tasks_count={len(self.mock_tasks)})"
