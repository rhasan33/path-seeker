import pytest

from path_seeker import PathSeeker, UnknownKeyProvided


def test_flat_dict() -> None:
    seeker = PathSeeker({"name": "Ada", "age": 30})
    assert seeker.find_last_value("name") == "Ada"


def test_returns_the_last_of_several_occurrences_across_depths() -> None:
    data = {"id": 1, "user": {"id": 2, "address": {"id": 3}}}
    seeker = PathSeeker(data)
    assert seeker.find_last_value("id") == 3


def test_returns_the_last_occurrence_inside_a_list_of_dicts() -> None:
    seeker = PathSeeker({"orders": [{"id": 1}, {"id": 2}]})
    assert seeker.find_last_value("id") == 2


def test_value_can_be_none() -> None:
    seeker = PathSeeker({"a": None})
    assert seeker.find_last_value("a") is None


def test_key_absent_raises_unknown_key_provided() -> None:
    with pytest.raises(UnknownKeyProvided, match="missing"):
        PathSeeker({"a": 1}).find_last_value("missing")


def test_empty_dict_raises_unknown_key_provided() -> None:
    with pytest.raises(UnknownKeyProvided):
        PathSeeker({}).find_last_value("anything")


def test_tuples_are_opaque_and_not_traversed() -> None:
    seeker = PathSeeker({"nested": ({"id": 1}, {"id": 2})})
    with pytest.raises(UnknownKeyProvided):
        seeker.find_last_value("id")
