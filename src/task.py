from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import logging

logger = logging.getLogger(__name__)

from src.exceptions import TaskIDError

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
            raise TaskIDError("Task id cannot be empty or None")
        logger.debug(f"Task created: id={self.id}")