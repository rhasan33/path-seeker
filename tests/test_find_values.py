import pytest

from path_seeker import PathSeeker


def test_flat_dict() -> None:
    seeker = PathSeeker({"name": "Ada", "age": 30})
    assert seeker.find_values("name") == ["Ada"]


def test_nested_dict() -> None:
    seeker = PathSeeker({"user": {"address": {"city": "Berlin"}}})
    assert seeker.find_values("city") == ["Berlin"]


def test_dict_containing_list_of_dicts() -> None:
    seeker = PathSeeker({"orders": [{"id": 1}, {"id": 2}]})
    assert seeker.find_values("id") == [1, 2]


def test_top_level_list_of_dicts() -> None:
    seeker = PathSeeker([{"id": 1}, {"id": 2, "nested": {"id": 3}}])
    assert seeker.find_values("id") == [1, 2, 3]


def test_key_at_multiple_depths() -> None:
    data = {"id": 1, "user": {"id": 2, "address": {"id": 3}}}
    seeker = PathSeeker(data)
    assert seeker.find_values("id") == [1, 2, 3]


def test_key_absent_returns_empty_list() -> None:
    seeker = PathSeeker({"a": 1})
    assert seeker.find_values("missing") == []


def test_empty_dict() -> None:
    assert PathSeeker({}).find_values("anything") == []


def test_empty_list() -> None:
    assert PathSeeker([]).find_values("anything") == []


def test_tuples_are_opaque_and_not_traversed() -> None:
    seeker = PathSeeker({"point": (1, 2), "nested": ({"id": 1}, {"id": 2})})
    # the tuple itself is a value that can be found under its own key...
    assert seeker.find_values("point") == [(1, 2)]
    # ...but dicts hidden inside a tuple are not traversed into
    assert seeker.find_values("id") == []


def test_value_can_be_any_type() -> None:
    data = {"a": None, "b": True, "c": 3.14, "d": [1, 2], "e": {"nested": 1}}
    seeker = PathSeeker(data)
    assert seeker.find_values("a") == [None]
    assert seeker.find_values("b") == [True]
    assert seeker.find_values("c") == [3.14]
    assert seeker.find_values("d") == [[1, 2]]
    assert seeker.find_values("e") == [{"nested": 1}]


@pytest.mark.parametrize("invalid", ["a string", 42, None, (1, 2), {1, 2}])
def test_non_dict_or_list_root_raises_type_error(invalid: object) -> None:
    with pytest.raises(TypeError):
        PathSeeker(invalid)  # type: ignore[arg-type]
