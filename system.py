from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, Iterator, runtime_checkable, Any
from pathlib import Path
import json
import uuid
import logging

logger = logging.getLogger(__name__)

@dataclass
class Task:
    """
    Единица работы в платформе обработки задач.

    """
    id: Any 
    payload: Any
    
    def __post_init__(self) -> None:
        """
        Валидация задачи после инициализации.

        """
        if not self.id:
            logger.error("Task validation failed: id cannot be empty or None")
            raise ValueError("Task id cannot be empty or None")
        logger.debug(f"Task created: id={self.id}")


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
            return
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
    logger.debug("Generating tasks")
    def get_tasks(self) -> Iterator[Task]:
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
    logger.debug("Returning tasks from API stub")
    def get_tasks(self) -> Iterator[Task]:
        for item in self.mock_tasks:
            yield Task(
                id=item["id"],
                payload=item.get("payload", {})
            )
    
    def __repr__(self) -> str:
        return f"APIStubTaskSource(tasks_count={len(self.mock_tasks)})"



class TaskReceiver:
    """
    Подсистема приёма задач.

    """
    
    def __init__(self) -> None:
        self._sources: list[TaskSource] = []
        self._tasks: list[Task] = []
        logger.debug("Task Receiver initialized")
    
    def add_source(self, source: TaskSource) -> None:
        if not isinstance(source, TaskSource):
            logger.error(
                f"Sourse {type(source).__name__} does not implement the TaskSource protocol"
                f"Expected method: get_tasks() -> Iterator[Task]"
            )
            raise TypeError(f"Sourse {type(source).__name__} does not implement the TaskSource protocol")

        self._sources.append(source)
        logger.info(f"Source {type(source).__name__} added")
    
    def fetch_all(self) -> list[Task]:
        logger.debug("fetch_all() called: clearing cache and loading tasks")
        self._tasks.clear()
        for source in self._sources:
            for task in source.get_tasks():
                self._tasks.append(task)
        return self._tasks
    
    @property
    def sources_count(self) -> int:
        """Количество источников"""
        return len(self._sources)
    
    @property
    def task_count(self) -> int:
        """Количество полученных задач после fetch_all"""
        return len(self._tasks)




def create_sample_file(filepath: str | Path, tasks: list[dict]) -> Path:
    """
    Создать тестовый JSON-файл

    """
    path = Path(filepath)
    logger.debug(f"Creating sample file: {path} with {len(tasks)} tasks")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)
    logger.info(f"Sample file created: {path}")
    return path


def validate_source(source: Any) -> bool:
    """
    Проверить объект на соответствие протоколу TaskSource

    """
    result = isinstance(source, TaskSource)
    logger.debug(f"validate_source({type(source).__name__}) = {result}")
    return result