"""
Исключения для модели задачи.

"""


class TaskValidationError(Exception):
    """
    Базовое исключение для ошибок валидации задачи.

    """
    pass


class TaskIDError(TaskValidationError):
    """Ошибка валидации идентификатора задачи."""
    pass

class TaskSourceValidationError(Exception):
    """
    Базовое исключение для ошибок валидации источников

    """
    pass