# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `find_first_value(key)` — the first value found under `key`, in traversal order; raises `UnknownKeyProvided` if absent.
- `find_last_value(key)` — the last value found under `key`, in traversal order; raises `UnknownKeyProvided` if absent.
- `update_first(key, new_value)` — update just the first occurrence of `key`, in traversal order.
- `update_last(key, new_value)` — update just the last occurrence of `key`, in traversal order.

## [0.1.0] - Unreleased

### Added

- `PathSeeker` class to search a nested `dict` or `list` of dicts by key.
- `find_values(key)` — every value found under `key`, at any depth.
- `find_paths(key)` — every `(path, value)` match for `key`, disambiguating duplicates.
- `get_keys()` — every distinct key name in the structure.
- `count_key(key)` — how many times `key` occurs.
- `set_value(path, new_value)` — update the value at an exact path, in place.
- `update_values(key, new_value)` — bulk-update every occurrence of `key`, in place.
