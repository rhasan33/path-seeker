from __future__ import annotations

from typing import Any, NamedTuple


class Match(NamedTuple):
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
