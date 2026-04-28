from __future__ import annotations
from typing import Any
from pathlib import Path
import json
import logging

from src.exceptions import TaskSourceValidationError
from src.sources import TaskSource
from src.task import Task


logger = logging.getLogger(__name__)


class TaskReceiver:
    """
    Подсистема приёма задач.

    """
    
    def __init__(self) -> None:
        self._sources: list[TaskSource] = []
        self._tasks: list[Task] = []
        logger.debug("Task Receiver initialized")
    
    def add_source(self, source: TaskSource) -> None:
        validate_source(source)
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


def validate_source(source: Any) -> None:
    """
    Проверить объект на соответствие протоколу TaskSource

    """
    if not isinstance(source, TaskSource):
        logger.error(f"Expected TaskSource, got {type(source).__name__}")
        raise TaskSourceValidationError(f"TaskSource validation failed: Expected TaskSource, got {type(source).__name__}")
    logger.debug(f"Task source is valid")