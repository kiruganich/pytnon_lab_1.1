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


## Структура проекта
task-sources-lab/
│
├── system.py # Основная логика (модели, источники, приёмник)
├── main.py # Точка входа для демонстрации
├── tests.py # Тесты (pytest)
├── requirements.txt # Зависимости
├── README.md # Этот файл
└── .gitignore # Игнорирование файлов Git

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
============================================================
Зарегистрировано источников: 3
Получено задач: 8
------------------------------------------------------------
  • ID: gen_0, Payload: {'step': 0, 'generated': True, 'source': 'generator'}
  • ID: gen_1, Payload: {'step': 1, 'generated': True, 'source': 'generator'}
  • ID: gen_2, Payload: {'step': 2, 'generated': True, 'source': 'generator'}
  • ID: api_1, Payload: {'source': 'stub', 'priority': 'high'}
  • ID: api_2, Payload: {'source': 'stub', 'priority': 'low'}
  • ID: api_3, Payload: {'source': 'stub', 'priority': 'medium'}
  • ID: file_1, Payload: {'source': 'json', 'priority': 'high'}
  • ID: file_2, Payload: {'source': 'json', 'priority': 'low'}
------------------------------------------------------------
Демонстрация завершена
============================================================
```
## Зависимости
Python 3.10+
pytest>=7.0.0
pytest-cov>=4.0.0 (опционально)
