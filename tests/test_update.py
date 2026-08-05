from typing import Any

import pytest

from path_seeker import PathSeeker


class TestSetValue:
    def test_updates_a_top_level_key(self) -> None:
        data = {"a": 1}
        seeker = PathSeeker(data)
        seeker.set_value(["a"], 2)
        assert seeker.data == {"a": 2}

    def test_updates_a_nested_key(self) -> None:
        data = {"user": {"address": {"city": "Berlin"}}}
        seeker = PathSeeker(data)
        seeker.set_value(["user", "address", "city"], "Munich")
        assert seeker.data == {"user": {"address": {"city": "Munich"}}}

    def test_updates_through_a_list_of_dicts(self) -> None:
        data: dict[str, Any] = {
            "orders": [{"id": 1, "status": "pending"}, {"id": 2, "status": "pending"}]
        }
        seeker = PathSeeker(data)
        seeker.set_value(["orders", 1, "status"], "shipped")
        assert data["orders"][1]["status"] == "shipped"
        assert data["orders"][0]["status"] == "pending"

    def test_disambiguates_duplicate_keys_via_exact_path(self) -> None:
        data = {"id": 1, "user": {"id": 2}}
        seeker = PathSeeker(data)
        seeker.set_value(["user", "id"], 99)
        assert seeker.data == {"id": 1, "user": {"id": 99}}

    def test_mutation_is_visible_on_the_caller_s_original_object(self) -> None:
        data = {"a": {"b": 1}}
        seeker = PathSeeker(data)
        seeker.set_value(["a", "b"], 2)
        assert data == {"a": {"b": 2}}

    def test_empty_path_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="empty"):
            PathSeeker({"a": 1}).set_value([], 2)

    def test_missing_dict_key_raises_key_error(self) -> None:
        with pytest.raises(KeyError):
            PathSeeker({"a": 1}).set_value(["missing"], 2)

    def test_out_of_range_index_raises_index_error(self) -> None:
        with pytest.raises(IndexError):
            PathSeeker({"items": [1, 2]}).set_value(["items", 5], 3)

    def test_int_index_into_dict_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="string key"):
            PathSeeker({"a": {"b": 1}}).set_value(["a", 0], 2)

    def test_string_key_into_list_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="int index"):
            PathSeeker({"items": [1, 2]}).set_value(["items", "b"], 3)

    def test_setting_the_tuple_itself_raises_value_error(self) -> None:
        # tuples are opaque (not traversed), so they can't be the final container either
        with pytest.raises(ValueError, match="cannot set a value inside"):
            PathSeeker({"point": (1, 2)}).set_value(["point", 0], 9)

    def test_stepping_through_a_tuple_raises_value_error(self) -> None:
        # an intermediate (non-final) step into a tuple hits _step_into instead
        with pytest.raises(ValueError, match="cannot index into"):
            PathSeeker({"point": (1, 2)}).set_value(["point", 0, "x"], 9)

    def test_missing_intermediate_dict_key_raises_key_error(self) -> None:
        with pytest.raises(KeyError):
            PathSeeker({"a": {"b": 1}}).set_value(["missing", "c"], 2)

    def test_intermediate_int_index_into_dict_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="string key"):
            PathSeeker({"a": {"b": 1}}).set_value([0, "c"], 2)

    def test_intermediate_string_key_into_list_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="int index"):
            PathSeeker(["a", "b"]).set_value(["x", "c"], 2)

    def test_intermediate_out_of_range_index_raises_index_error(self) -> None:
        with pytest.raises(IndexError):
            PathSeeker(["a", "b"]).set_value([5, "c"], 2)

    def test_setting_a_tuple_as_the_final_value_is_fine(self) -> None:
        # the tuple is only opaque to traversal; it's still a valid value to *set*
        data: dict[str, Any] = {"point": (1, 2)}
        seeker = PathSeeker(data)
        seeker.set_value(["point"], (3, 4))
        assert data == {"point": (3, 4)}


class TestUpdateValues:
    def test_updates_the_single_occurrence(self) -> None:
        seeker = PathSeeker({"a": 1})
        updated = seeker.update_values("a", 2)
        assert updated == 1
        assert seeker.data == {"a": 2}

    def test_bulk_updates_every_occurrence_across_depths(self) -> None:
        data = {"id": 1, "user": {"id": 2, "address": {"id": 3}}}
        seeker = PathSeeker(data)
        updated = seeker.update_values("id", 0)
        assert updated == 3
        assert seeker.find_values("id") == [0, 0, 0]

    def test_updates_inside_a_list_of_dicts(self) -> None:
        data: dict[str, Any] = {"orders": [{"status": "pending"}, {"status": "pending"}]}
        seeker = PathSeeker(data)
        updated = seeker.update_values("status", "cancelled")
        assert updated == 2
        assert all(order["status"] == "cancelled" for order in data["orders"])

    def test_key_absent_updates_nothing(self) -> None:
        data = {"a": 1}
        seeker = PathSeeker(data)
        assert seeker.update_values("missing", 2) == 0
        assert data == {"a": 1}

    def test_keys_hidden_inside_a_tuple_are_not_updated(self) -> None:
        data: dict[str, Any] = {"nested": ({"id": 1}, {"id": 2})}
        seeker = PathSeeker(data)
        assert seeker.update_values("id", 0) == 0
        assert data == {"nested": ({"id": 1}, {"id": 2})}
