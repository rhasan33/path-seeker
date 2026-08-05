from __future__ import annotations

from collections.abc import Iterator
from typing import Any, NamedTuple


class Match(NamedTuple):
    path: list[str | int]
    value: Any


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
