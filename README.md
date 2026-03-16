# Система приёма задач — Лабораторная работа №1

## Описание

Реализация подсистему приёма задач в платформе обработки задач с использованием duck typing и контрактного программирования через typing.Protocol.

### Основной функционал:
- Duck typing через Protocol: источники задач не связаны наследованием
- Единый контракт: все источники реализуют get_tasks() -> Iterator[Task]
- Ленивая загрузка через Iterator
- Runtime-проверка: isinstance() с @runtime_checkable
- Три типа источников: файл, генератор, API-заглушка
- Расширяемость: новые источники без изменения существующего кода
- Покрытие тестами
- Логирование


## Структура проекта
```
task-sources-lab/
│
├── system.py # Основная логика (модели, источники, приёмник)
├── main.py # Точка входа для демонстрации
├── tests.py # Тесты (pytest)
├── requirements.txt # Зависимости
├── README.md # Этот файл
└── .gitignore # Игнорирование файлов Git
```

## Установка и запуск

### 1. Требования
- Python 3.10+ (для синтаксиса str | int)
- pytest 7.0.0+

### 2. Установка зависимостей
pip install -r requirements.txt
### 3. Запуск демонстрации
python main.py
### 4. Запуск тестов
pytest tests.py

## Пример работы
```
2026-03-06 23:13:54,783 - INFO - Starting programm
2026-03-06 23:13:54,783 - INFO - Source GeneratorTaskSource added
2026-03-06 23:13:54,783 - INFO - Source APIStubTaskSource added
2026-03-06 23:13:54,784 - INFO - Sample file created: demo_tasks.json
2026-03-06 23:13:54,784 - INFO - Source FileTaskSource added
2026-03-06 23:13:54,784 - INFO - Fetching all tasks...
2026-03-06 23:13:54,784 - INFO - Finished generating 3 tasks
2026-03-06 23:13:54,786 - INFO - Finished reading 2 tasks from demo_tasks.json
2026-03-06 23:13:54,786 - INFO - ============================================================
2026-03-06 23:13:54,786 - INFO - Зарегистрировано источников: 3
2026-03-06 23:13:54,786 - INFO - Получено задач: 8
2026-03-06 23:13:54,786 - INFO - ------------------------------------------------------------
2026-03-06 23:13:54,786 - INFO -   • ID: gen_0, Payload: {'step': 0, 'generated': True, 'source': 'generator'}
2026-03-06 23:13:54,786 - INFO -   • ID: gen_1, Payload: {'step': 1, 'generated': True, 'source': 'generator'}
2026-03-06 23:13:54,786 - INFO -   • ID: gen_2, Payload: {'step': 2, 'generated': True, 'source': 'generator'}
2026-03-06 23:13:54,787 - INFO -   • ID: api_1, Payload: {'source': 'stub', 'priority': 'high'}
2026-03-06 23:13:54,787 - INFO -   • ID: api_2, Payload: {'source': 'stub', 'priority': 'low'}
2026-03-06 23:13:54,787 - INFO -   • ID: api_3, Payload: {'source': 'stub', 'priority': 'medium'}
2026-03-06 23:13:54,788 - INFO -   • ID: file_1, Payload: {'source': 'json', 'priority': 'high'}
2026-03-06 23:13:54,788 - INFO -   • ID: file_2, Payload: {'source': 'json', 'priority': 'low'}
2026-03-06 23:13:54,788 - INFO - ------------------------------------------------------------
2026-03-06 23:13:54,788 - INFO - Демонстрация завершена
2026-03-06 23:13:54,788 - INFO - ============================================================
```
## Зависимости
Python 3.10+
pytest>=7.0.0
pytest-cov>=4.0.0 (опционально)
