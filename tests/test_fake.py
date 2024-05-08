import pytest

from app.utils.addition import add_two_numbers


@pytest.mark.skip(reason="no way of currently testing this")
def test_add_two_numbers():
    result = add_two_numbers(1.1, 2)
    assert result == 3.1
    assert isinstance(result, float)
