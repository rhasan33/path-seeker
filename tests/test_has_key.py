from path_seeker import PathSeeker


def test_key_present_at_top_level() -> None:
    seeker = PathSeeker({"name": "Ada", "age": 30})
    assert seeker.has_key("name") is True


def test_key_present_at_nested_depth() -> None:
    data = {"user": {"address": {"city": "Berlin"}}}
    seeker = PathSeeker(data)
    assert seeker.has_key("city") is True


def test_key_absent() -> None:
    seeker = PathSeeker({"name": "Ada"})
    assert seeker.has_key("missing") is False


def test_key_present_only_inside_list_of_dicts() -> None:
    seeker = PathSeeker({"orders": [{"id": 100, "status": "shipped"}]})
    assert seeker.has_key("status") is True


def test_empty_dict_and_list_have_no_keys() -> None:
    assert PathSeeker({}).has_key("anything") is False
    assert PathSeeker([]).has_key("anything") is False
