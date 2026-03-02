import pytest
import json
import tempfile
from pathlib import Path
from typing import Iterator

from system import (
    Task,
    TaskSource,
    FileTaskSource,
    GeneratorTaskSource,
    APIStubTaskSource,
    TaskReceiver,
    create_sample_file,
)



class TestTask:
    """Тесты класса Task."""
    
    def test_task_creation(self):
        task = Task(id="test_1", payload={"key": "value"})
        assert task.id == "test_1"
        assert task.payload == {"key": "value"}
    
    def test_task_empty_id_raises_error(self):
        with pytest.raises(ValueError):
            Task(id="", payload={})


class TestProtocol:
    """Тесты протокола TaskSource и duck typing."""
    
    def test_generator_source_is_task_source(self):
        source = GeneratorTaskSource()
        assert isinstance(source, TaskSource)
    
    def test_custom_source_without_inheritance(self):
        class CustomSource:
            def get_tasks(self) -> Iterator[Task]:
                yield Task(id="custom", payload={})
        
        custom = CustomSource()
        assert isinstance(custom, TaskSource)
    
    def test_invalid_source_not_task_source(self):
        class BadSource:
            pass
        
        assert not isinstance(BadSource(), TaskSource)


class TestSources:
    """Тесты источников задач."""
    
    def test_generator_count(self):
        source = GeneratorTaskSource(count=5)
        tasks = list(source.get_tasks())
        assert len(tasks) == 5
    
    def test_api_stub_default_tasks(self):
        source = APIStubTaskSource()
        tasks = list(source.get_tasks())
        assert len(tasks) == 3
    
    def test_file_source_valid_file(self):
        data = [{"id": "file_1", "payload": {"test": 1}}]
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            temp_path = f.name
        
        try:
            source = FileTaskSource(temp_path)
            tasks = list(source.get_tasks())
            assert len(tasks) == 1
        finally:
            Path(temp_path).unlink()


class TestTaskReceiver:
    """Тесты TaskReceiver."""
    
    def test_receiver_add_source(self):
        receiver = TaskReceiver()
        source = GeneratorTaskSource(count=3)
        receiver.add_source(source)
        assert receiver.sources_count == 1
    
    def test_receiver_add_invalid_source(self):
        receiver = TaskReceiver()
        
        class BadSource:
            pass
        
        with pytest.raises(TypeError):
            receiver.add_source(BadSource())
    
    def test_receiver_fetch_all(self):
        receiver = TaskReceiver()
        receiver.add_source(GeneratorTaskSource(count=3))
        receiver.add_source(APIStubTaskSource())
        tasks = receiver.fetch_all()
        assert receiver.task_count == 6  # 3 + 3


class TestExtensibility:
    """Тесты архитектурной расширяемости."""
    
    def test_new_source_without_code_changes(self):
        class NewSource:
            def get_tasks(self) -> Iterator[Task]:
                yield Task(id="new_1", payload={"source": "new"})
        
        receiver = TaskReceiver()
        receiver.add_source(NewSource())
        tasks = receiver.fetch_all()
        
        assert len(tasks) == 1
        assert tasks[0].payload.get("source") == "new"