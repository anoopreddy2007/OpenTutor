import pytest

from app.services.bkt_validation import validate_response_sequence


def test_valid_response_sequence():
    responses = [True, False, True]

    assert validate_response_sequence(responses) == responses


def test_empty_response_sequence():
    assert validate_response_sequence([]) == []


def test_non_boolean_response_is_rejected():
    with pytest.raises(ValueError):
        validate_response_sequence([True, 1, False])


def test_non_list_input_is_rejected():
    with pytest.raises(TypeError):
        validate_response_sequence((True, False))