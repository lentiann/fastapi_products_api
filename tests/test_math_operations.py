import pytest

from app.utils.addition import add_two_numbers, throw_error_function


def test_add_two_numbers():
    result = add_two_numbers(1.1, 2)
    assert result == 3.1
    assert isinstance(result, float)


def test_add_two_numbers_with_none_value():
    with pytest.raises(TypeError):
        add_two_numbers(1.1, None)


def test_throw_error_function():
    with pytest.raises(ValueError):
        throw_error_function()
