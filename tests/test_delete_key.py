from path_seeker import PathSeeker


class TestDeleteKey:
    def test_deletes_the_single_occurrence(self) -> None:
        seeker = PathSeeker({"name": "Ada", "age": 30})
        assert seeker.delete_key("age") == 1
        assert seeker.data == {"name": "Ada"}

    def test_deletes_every_occurrence_across_depths(self) -> None:
        data = {"id": 1, "user": {"id": 2, "address": {"id": 3}}}
        seeker = PathSeeker(data)
        assert seeker.delete_key("id") == 3
        assert seeker.data == {"user": {"address": {}}}

    def test_deletes_from_a_list_of_dicts(self) -> None:
        data = {"orders": [{"id": 1, "status": "shipped"}, {"id": 2, "status": "pending"}]}
        seeker = PathSeeker(data)
        assert seeker.delete_key("status") == 2
        assert seeker.data == {"orders": [{"id": 1}, {"id": 2}]}

    def test_key_absent_deletes_nothing_and_returns_zero(self) -> None:
        data = {"a": 1}
        seeker = PathSeeker(data)
        assert seeker.delete_key("missing") == 0
        assert seeker.data == {"a": 1}

    def test_empty_dict_and_list_delete_nothing(self) -> None:
        assert PathSeeker({}).delete_key("anything") == 0
        assert PathSeeker([]).delete_key("anything") == 0

    def test_mutation_is_visible_on_the_caller_s_original_object(self) -> None:
        original = {"a": 1, "b": 2}
        seeker = PathSeeker(original)
        seeker.delete_key("a")
        assert original == {"b": 2}

    def test_many_duplicate_occurrences_do_not_raise_during_traversal(self) -> None:
        data = {f"item{i}": {"tag": i} for i in range(50)}
        seeker = PathSeeker(data)
        assert seeker.delete_key("tag") == 50
        assert all("tag" not in value for value in data.values())


class TestDeleteFirst:
    def test_deletes_the_single_occurrence(self) -> None:
        data = {"a": 1}
        seeker = PathSeeker(data)
        assert seeker.delete_first("a") is True
        assert data == {}

    def test_deletes_only_the_first_of_several_occurrences_across_depths(self) -> None:
        data = {"id": 1, "user": {"id": 2, "address": {"id": 3}}}
        seeker = PathSeeker(data)
        assert seeker.delete_first("id") is True
        assert data == {"user": {"id": 2, "address": {"id": 3}}}

    def test_deletes_only_the_first_occurrence_inside_a_list_of_dicts(self) -> None:
        data = {"orders": [{"status": "pending"}, {"status": "pending"}]}
        seeker = PathSeeker(data)
        assert seeker.delete_first("status") is True
        assert data == {"orders": [{}, {"status": "pending"}]}

    def test_key_absent_returns_false_and_deletes_nothing(self) -> None:
        data = {"a": 1}
        seeker = PathSeeker(data)
        assert seeker.delete_first("missing") is False
        assert data == {"a": 1}

    def test_mutation_is_visible_on_the_caller_s_original_object(self) -> None:
        original = {"a": 1, "b": 2}
        seeker = PathSeeker(original)
        seeker.delete_first("a")
        assert original == {"b": 2}


class TestDeleteLast:
    def test_deletes_the_single_occurrence(self) -> None:
        data = {"a": 1}
        seeker = PathSeeker(data)
        assert seeker.delete_last("a") is True
        assert data == {}

    def test_deletes_only_the_last_of_several_occurrences_across_depths(self) -> None:
        data = {"id": 1, "user": {"id": 2, "address": {"id": 3}}}
        seeker = PathSeeker(data)
        assert seeker.delete_last("id") is True
        assert data == {"id": 1, "user": {"id": 2, "address": {}}}

    def test_deletes_only_the_last_occurrence_inside_a_list_of_dicts(self) -> None:
        data = {"orders": [{"status": "pending"}, {"status": "pending"}]}
        seeker = PathSeeker(data)
        assert seeker.delete_last("status") is True
        assert data == {"orders": [{"status": "pending"}, {}]}

    def test_key_absent_returns_false_and_deletes_nothing(self) -> None:
        data = {"a": 1}
        seeker = PathSeeker(data)
        assert seeker.delete_last("missing") is False
        assert data == {"a": 1}

    def test_mutation_is_visible_on_the_caller_s_original_object(self) -> None:
        original = {"a": 1, "b": 2}
        seeker = PathSeeker(original)
        seeker.delete_last("b")
        assert original == {"a": 1}
