# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.0] - 2026-08-05

### Added

- `delete_first(key)` — delete just the first occurrence of `key`, in traversal order; returns `False` if absent.
- `delete_last(key)` — delete just the last occurrence of `key`, in traversal order; returns `False` if absent.

## [0.3.0] - 2026-08-05

### Added

- `has_key(key)` — whether `key` occurs anywhere in the structure.
- `find_first_path(key)` — the first `(path, value)` match found under `key`, in traversal order; raises `UnknownKeyProvided` if absent.
- `find_last_path(key)` — the last `(path, value)` match found under `key`, in traversal order; raises `UnknownKeyProvided` if absent.
- `delete_key(key)` — delete every occurrence of `key`, at any depth; returns count deleted.

## [0.2.0] - 2026-08-05

### Added

- `find_first_value(key)` — the first value found under `key`, in traversal order; raises `UnknownKeyProvided` if absent.
- `find_last_value(key)` — the last value found under `key`, in traversal order; raises `UnknownKeyProvided` if absent.
- `update_first(key, new_value)` — update just the first occurrence of `key`, in traversal order.
- `update_last(key, new_value)` — update just the last occurrence of `key`, in traversal order.

## [0.1.0] - 2026-08-05

### Added

- `PathSeeker` class to search a nested `dict` or `list` of dicts by key.
- `find_values(key)` — every value found under `key`, at any depth.
- `find_paths(key)` — every `(path, value)` match for `key`, disambiguating duplicates.
- `get_keys()` — every distinct key name in the structure.
- `count_key(key)` — how many times `key` occurs.
- `set_value(path, new_value)` — update the value at an exact path, in place.
- `update_values(key, new_value)` — bulk-update every occurrence of `key`, in place.
