import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

from system import (
    Task,
    FileTaskSource,
    GeneratorTaskSource,
    APIStubTaskSource,
    TaskReceiver,
    create_sample_file,
)
from pathlib import Path

logger = logging.getLogger(__name__)

def main() -> None:
    logger.info("Starting programm")
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

    logger.info("Fetching all tasks...")
    tasks = receiver.fetch_all()
    
    logger.info("=" * 60)
    logger.info(f"Зарегистрировано источников: {receiver.sources_count}")
    logger.info(f"Получено задач: {receiver.task_count}")
    logger.info("-" * 60)
    
    for task in tasks:
        logger.info(f"  • ID: {task.id}, Payload: {task.payload}")
    
    logger.info("-" * 60)
    logger.info("Демонстрация завершена")
    logger.info("=" * 60)

    test_file.unlink()
    logger.debug(f"Temporary file removed: {test_file}")


if __name__ == "__main__":
    main()