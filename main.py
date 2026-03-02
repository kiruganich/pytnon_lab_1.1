from system import (
    Task,
    FileTaskSource,
    GeneratorTaskSource,
    APIStubTaskSource,
    TaskReceiver,
    create_sample_file,
)
from pathlib import Path


def main() -> None:

    receiver = TaskReceiver()

    sources = [
        GeneratorTaskSource(count=3, prefix="gen"),
        APIStubTaskSource(),
    ]
    
    for source in sources:
        receiver.add_source(source)

    test_file = Path("demo_tasks.json")
    sample_data = [
        {"id": "file_1", "payload": {"source": "json", "priority": "high"}},
        {"id": "file_2", "payload": {"source": "json", "priority": "low"}},
    ]
    create_sample_file(test_file, sample_data)
    receiver.add_source(FileTaskSource(test_file))

    tasks = receiver.fetch_all()
    
    print("=" * 60)
    print(f"Зарегистрировано источников: {receiver.sources_count}")
    print(f"Получено задач: {receiver.task_count}")
    print("-" * 60)
    
    for task in tasks:
        print(f"  • ID: {task.id}, Payload: {task.payload}")
    
    print("-" * 60)
    print("Демонстрация завершена")
    print("=" * 60)

    test_file.unlink()


if __name__ == "__main__":
    main()