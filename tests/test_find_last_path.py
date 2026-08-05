import pytest

from path_seeker import Match, PathSeeker, UnknownKeyProvided


def test_flat_dict() -> None:
    seeker = PathSeeker({"name": "Ada"})
    assert seeker.find_last_path("name") == Match(["name"], "Ada")


def test_returns_the_last_of_several_occurrences_across_depths() -> None:
    data = {"id": 1, "user": {"id": 2, "address": {"id": 3}}}
    seeker = PathSeeker(data)
    assert seeker.find_last_path("id") == Match(["user", "address", "id"], 3)


def test_returns_the_last_occurrence_inside_a_list_of_dicts() -> None:
    seeker = PathSeeker({"orders": [{"id": 1}, {"id": 2}]})
    assert seeker.find_last_path("id") == Match(["orders", 1, "id"], 2)


def test_key_absent_raises_unknown_key_provided() -> None:
    with pytest.raises(UnknownKeyProvided, match="missing"):
        PathSeeker({"a": 1}).find_last_path("missing")


def test_empty_dict_raises_unknown_key_provided() -> None:
    with pytest.raises(UnknownKeyProvided):
        PathSeeker({}).find_last_path("anything")
