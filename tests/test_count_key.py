from path_seeker import PathSeeker


def test_key_absent_is_zero() -> None:
    assert PathSeeker({"a": 1}).count_key("missing") == 0


def test_single_occurrence() -> None:
    assert PathSeeker({"a": 1}).count_key("a") == 1


def test_duplicate_key_at_multiple_depths() -> None:
    data = {"id": 1, "user": {"id": 2, "address": {"id": 3}}}
    assert PathSeeker(data).count_key("id") == 3


def test_agrees_with_len_of_find_values() -> None:
    data = {"orders": [{"id": 1}, {"id": 2}, {"id": 3, "nested": {"id": 4}}]}
    seeker = PathSeeker(data)
    assert seeker.count_key("id") == len(seeker.find_values("id"))


def test_empty_structure() -> None:
    assert PathSeeker({}).count_key("anything") == 0
    assert PathSeeker([]).count_key("anything") == 0
