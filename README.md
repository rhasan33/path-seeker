# path-seeker

[![CI](https://github.com/rhasan33/path-seeker/actions/workflows/ci.yml/badge.svg)](https://github.com/rhasan33/path-seeker/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/path-seeker.svg)](https://pypi.org/project/path-seeker/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Find, count, and update keys anywhere in a nested `dict` or `list` of dicts — with
full path disambiguation when the same key occurs at multiple depths.

## Installation

```bash
pip install path-seeker
```

## Usage

```python
from path_seeker import PathSeeker

data = {
    "user": {
        "id": 1,
        "address": {"id": 42, "city": "Berlin"},
    },
    "orders": [
        {"id": 100, "status": "shipped"},
        {"id": 101, "status": "pending"},
    ],
}

seeker = PathSeeker(data)

# All values found under a key, at any depth
seeker.find_values("id")
# [1, 42, 100, 101]

# All (path, value) matches — use this to disambiguate duplicates
seeker.find_paths("id")
# [Match(path=['user', 'id'], value=1),
#  Match(path=['user', 'address', 'id'], value=42),
#  Match(path=['orders', 0, 'id'], value=100),
#  Match(path=['orders', 1, 'id'], value=101)]

# The first/last value found under a key, in traversal order
seeker.find_first_value("id")
# 1
seeker.find_last_value("id")
# 101

# Every distinct key name in the structure
seeker.get_keys()
# ['address', 'city', 'id', 'orders', 'status', 'user']

# How many times a key occurs
seeker.count_key("id")
# 4

# Update one exact occurrence, using a path from find_paths
seeker.set_value(["orders", 1, "status"], "cancelled")

# Update every occurrence of a key at once
seeker.update_values("id", 0)
# 4  (number of occurrences updated)

# Update just the first/last occurrence, in traversal order
seeker.update_first("id", -1)
# True
seeker.update_last("id", -2)
# True
```

## API

| Method | Returns | Description |
| --- | --- | --- |
| `find_values(key)` | `list[Any]` | Every value stored under `key`, at any depth. |
| `find_paths(key)` | `list[Match]` | Every `(path, value)` pair for `key`, at any depth. |
| `find_first_value(key)` | `Any` | The first value found under `key`, in traversal order. Raises `UnknownKeyProvided` if `key` doesn't occur anywhere. |
| `find_last_value(key)` | `Any` | The last value found under `key`, in traversal order. Raises `UnknownKeyProvided` if `key` doesn't occur anywhere. |
| `get_keys()` | `list[str]` | Every distinct key name in the structure, sorted. |
| `count_key(key)` | `int` | How many times `key` occurs. |
| `set_value(path, new_value)` | `None` | Update the value at an exact path (from `find_paths`). |
| `update_values(key, new_value)` | `int` | Update every occurrence of `key`; returns count updated. |
| `update_first(key, new_value)` | `bool` | Update the first occurrence of `key`, in traversal order; `False` if absent. |
| `update_last(key, new_value)` | `bool` | Update the last occurrence of `key`, in traversal order; `False` if absent. |
| `.data` | `dict \| list` | The current (possibly mutated) underlying structure. |

Search is by **key name**, not by value — searching for a value and getting its path
back is not supported yet.

## Limitations

- `PathSeeker` holds a reference to the structure you pass in — it does not make a
  defensive copy, so updates via `set_value`/`update_values` mutate your original
  object too.
- Nested `dict`s and `list`s are traversed; other iterables (tuples, sets,
  generators) are treated as opaque values, since list-index-style paths don't make
  sense for them.
- No cycle detection. This is fine for JSON/YAML-shaped data, which can't contain
  cycles, but a structure with a manually-introduced reference cycle will recurse
  forever.

## Development

```bash
make install      # uv sync --all-extras
make check        # lint + typecheck + test (what CI runs)
```

Individual targets: `make test`, `make lint`, `make format`, `make typecheck`.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow.

## License

MIT — see [LICENSE](LICENSE).
