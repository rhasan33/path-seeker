from path_seeker import PathSeeker


def test_flat_dict_keys() -> None:
    seeker = PathSeeker({"name": "Ada", "age": 30})
    assert seeker.get_keys() == ["age", "name"]


def test_nested_and_repeated_keys_are_deduplicated() -> None:
    data = {
        "user": {"id": 1, "address": {"id": 2, "city": "Berlin"}},
        "orders": [{"id": 3, "status": "shipped"}],
    }
    seeker = PathSeeker(data)
    assert seeker.get_keys() == ["address", "city", "id", "orders", "status", "user"]


def test_top_level_list_of_dicts_keys() -> None:
    seeker = PathSeeker([{"a": 1}, {"b": 2}])
    assert seeker.get_keys() == ["a", "b"]


def test_empty_dict_and_list_have_no_keys() -> None:
    assert PathSeeker({}).get_keys() == []
    assert PathSeeker([]).get_keys() == []


def test_list_indices_are_not_reported_as_keys() -> None:
    seeker = PathSeeker({"items": [1, 2, 3]})
    assert seeker.get_keys() == ["items"]
