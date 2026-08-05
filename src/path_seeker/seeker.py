from __future__ import annotations

from collections.abc import Iterator
from typing import Any, NamedTuple


class Match(NamedTuple):
    path: list[str | int]
    value: Any


class UnknownKeyProvided(KeyError):  # noqa: N818
    def __init__(self, key: str) -> None:
        super().__init__(f"key {key!r} was not found in the structure")
        self.key = key


class _Entry(NamedTuple):
    """One dict key/value pair found during traversal, with enough context to
    both report it (path, value) and mutate it in place (parent, key)."""

    parent: dict[str, Any]
    key: str
    path: list[str | int]
    value: Any


class PathSeeker:
    def __init__(self, data: dict[str, Any] | list[Any]) -> None:
        if not isinstance(data, (dict, list)):
            raise TypeError(
                f"PathSeeker requires a dict or list at the root, got {type(data).__name__}"
            )
        self._data = data

    @property
    def data(self) -> dict[str, Any] | list[Any]:
        return self._data

    def _entries(self) -> Iterator[_Entry]:
        """Walk the whole structure, yielding one `_Entry` per dict key/value
        pair at any depth. Every read-only method (`find_values`, `find_paths`,
        `get_keys`, `count_key`) and every mutating method (`update_values`)
        is built on top of this single traversal."""

        def walk(node: Any, path: list[str | int]) -> Iterator[_Entry]:
            if isinstance(node, dict):
                for child_key, child_value in node.items():
                    child_path = [*path, child_key]
                    yield _Entry(node, child_key, child_path, child_value)
                    yield from walk(child_value, child_path)
            elif isinstance(node, list):
                for index, item in enumerate(node):
                    yield from walk(item, [*path, index])

        yield from walk(self._data, [])

    def find_values(self, key: str) -> list[Any]:
        return [entry.value for entry in self._entries() if entry.key == key]

    def find_paths(self, key: str) -> list[Match]:
        return [Match(entry.path, entry.value) for entry in self._entries() if entry.key == key]

    def find_first_path(self, key: str) -> Match:
        for entry in self._entries():
            if entry.key == key:
                return Match(entry.path, entry.value)
        raise UnknownKeyProvided(key)

    def find_last_path(self, key: str) -> Match:
        last_match: Match | None = None
        for entry in self._entries():
            if entry.key == key:
                last_match = Match(entry.path, entry.value)
        if last_match is None:
            raise UnknownKeyProvided(key)
        return last_match

    def find_first_value(self, key: str) -> Any:
        for entry in self._entries():
            if entry.key == key:
                return entry.value
        raise UnknownKeyProvided(key)

    def find_last_value(self, key: str) -> Any:
        found = False
        value: Any = None
        for entry in self._entries():
            if entry.key == key:
                found = True
                value = entry.value
        if not found:
            raise UnknownKeyProvided(key)
        return value

    def get_keys(self) -> list[str]:
        return sorted({entry.key for entry in self._entries()})

    def count_key(self, key: str) -> int:
        return sum(1 for entry in self._entries() if entry.key == key)

    def has_key(self, key: str) -> bool:
        return any(entry.key == key for entry in self._entries())

    def set_value(self, path: list[str | int], new_value: Any) -> None:
        if not path:
            raise ValueError("path must not be empty")
        container: Any = self._data
        for step in path[:-1]:
            container = self._step_into(container, step)
        last = path[-1]
        if isinstance(container, dict):
            if not isinstance(last, str):
                raise ValueError(f"expected a string key for dict, got {type(last).__name__}")
            if last not in container:
                raise KeyError(last)
        elif isinstance(container, list):
            if not isinstance(last, int) or isinstance(last, bool):
                raise ValueError(f"expected an int index for list, got {type(last).__name__}")
            if not -len(container) <= last < len(container):
                raise IndexError(last)
        else:
            raise ValueError(f"cannot set a value inside {type(container).__name__}")
        container[last] = new_value

    def update_values(self, key: str, new_value: Any) -> int:
        count = 0
        for entry in self._entries():
            if entry.key == key:
                entry.parent[entry.key] = new_value
                count += 1
        return count

    def update_first(self, key: str, new_value: Any) -> bool:
        for entry in self._entries():
            if entry.key == key:
                entry.parent[entry.key] = new_value
                return True
        return False

    def update_last(self, key: str, new_value: Any) -> bool:
        last_entry = None
        for entry in self._entries():
            if entry.key == key:
                last_entry = entry
        if last_entry is None:
            return False
        last_entry.parent[last_entry.key] = new_value
        return True

    @staticmethod
    def _step_into(container: Any, step: str | int) -> Any:
        if isinstance(container, dict):
            if not isinstance(step, str):
                raise ValueError(f"expected a string key for dict, got {type(step).__name__}")
            if step not in container:
                raise KeyError(step)
            return container[step]
        if isinstance(container, list):
            if not isinstance(step, int) or isinstance(step, bool):
                raise ValueError(f"expected an int index for list, got {type(step).__name__}")
            if not -len(container) <= step < len(container):
                raise IndexError(step)
            return container[step]
        raise ValueError(f"cannot index into {type(container).__name__}")
