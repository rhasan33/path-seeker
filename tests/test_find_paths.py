from path_seeker import Match, PathSeeker


def test_flat_dict() -> None:
    seeker = PathSeeker({"name": "Ada"})
    assert seeker.find_paths("name") == [Match(["name"], "Ada")]


def test_nested_dict_path() -> None:
    seeker = PathSeeker({"user": {"address": {"city": "Berlin"}}})
    assert seeker.find_paths("city") == [Match(["user", "address", "city"], "Berlin")]


def test_path_through_list_of_dicts() -> None:
    seeker = PathSeeker({"orders": [{"id": 1}, {"id": 2}]})
    assert seeker.find_paths("id") == [
        Match(["orders", 0, "id"], 1),
        Match(["orders", 1, "id"], 2),
    ]


def test_top_level_list_of_dicts_paths() -> None:
    seeker = PathSeeker([{"id": 1}, {"id": 2}])
    assert seeker.find_paths("id") == [Match([0, "id"], 1), Match([1, "id"], 2)]


def test_duplicate_key_at_multiple_depths_is_disambiguated_by_path() -> None:
    data = {"id": 1, "user": {"id": 2, "address": {"id": 3}}}
    seeker = PathSeeker(data)
    matches = seeker.find_paths("id")
    assert matches == [
        Match(["id"], 1),
        Match(["user", "id"], 2),
        Match(["user", "address", "id"], 3),
    ]
    # every match has a distinct path even though the key repeats
    assert len({tuple(m.path) for m in matches}) == len(matches)


def test_key_absent_returns_empty_list() -> None:
    assert PathSeeker({"a": 1}).find_paths("missing") == []


def test_empty_dict_and_list() -> None:
    assert PathSeeker({}).find_paths("anything") == []
    assert PathSeeker([]).find_paths("anything") == []
