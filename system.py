from __future__ import annotations
from dataclasses import dataclass, field
from typing import Protocol, Iterator, runtime_checkable, Any
from pathlib import Path
import json
import uuid


@dataclass
class Task:
    """
    Единица работы в платформе обработки задач.

    """
    id: str | int
    payload: dict = field(default_factory=dict)
    
    def __post_init__(self) -> None:
        """
        Валидация задачи после инициализации.

        """
        if not self.id:
            raise ValueError("Task id cannot be empty or None")


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
    
    def get_tasks(self) -> Iterator[Task]:
        if not self.filepath.exists():
            return
        
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                yield Task(
                    id=item["id"],
                    payload=item.get("payload", {})
                )


class GeneratorTaskSource:
    """
    Источник задач - программная генерация.

    """
    
    def __init__(self, count: int = 5, prefix: str = "gen") -> None:
        self.count = count
        self.prefix = prefix
    
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
    
    def add_source(self, source: TaskSource) -> None:
        if not isinstance(source, TaskSource):
            raise TypeError(
                f"Источник {type(source).__name__} не соответствует протоколу TaskSource"
                f"Ожидаемый метод: get_tasks() -> Iterator[Task]"
            )
        self._sources.append(source)
    
    def fetch_all(self) -> list[Task]:
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
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)
    return path


def validate_source(source: Any) -> bool:
    """
    Проверить объект на соответствие протоколу TaskSource

    """
    return isinstance(source, TaskSource)