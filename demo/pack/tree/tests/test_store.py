import pytest

from taskflow.models import TaskflowError
from taskflow.services.store import TaskStore


def test_add_and_list_sorted(tmp_path) -> None:
    store = TaskStore(data_file=tmp_path / "tasks.json")
    store.add("first")
    store.add("second")
    titles = [task.title for task in store.list()]
    assert titles == ["first", "second"]


def test_persists_across_instances(tmp_path) -> None:
    path = tmp_path / "tasks.json"
    TaskStore(data_file=path).add("persist me")
    titles = [task.title for task in TaskStore(data_file=path).list()]
    assert titles == ["persist me"]


def test_mark_done_and_remove(tmp_path) -> None:
    store = TaskStore(data_file=tmp_path / "tasks.json")
    task = store.add("one")
    store.mark_done(task.id)
    assert store.get(task.id).done is True
    store.remove(task.id)
    with pytest.raises(TaskflowError):
        store.get(task.id)


def test_rejects_empty_title(tmp_path) -> None:
    store = TaskStore(data_file=tmp_path / "tasks.json")
    with pytest.raises(TaskflowError):
        store.add("   ")
