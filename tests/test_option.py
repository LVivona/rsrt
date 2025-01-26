import pytest
from rsrt import Option, Some, NoneType

def add(x : int ,y : int) -> Option[int]:
    return Some(x + y)

def uadd(x : int, y : int) -> Option[int]:
    if x < 0 or y < 0:
        return NoneType
    return Some(x + y)

def test_add():
    """Test the add function with valid inputs."""
    result = add(2, 3)
    assert isinstance(result, Some)
    assert result.is_some() is True
    assert result.is_none() is False
    assert result.unwrap() == 5

def test_uadd_positive_numbers():
    """Test the uadd function with valid inputs."""
    result = uadd(3, 4)
    assert isinstance(result, Some)
    assert result.is_some() is True
    assert result.is_none() is False
    assert result.unwrap() == 7

def test_uadd_negative_numbers():
    """Test the uadd function with invalid inputs."""
    result = uadd(-1, 4)
    assert result is NoneType
    assert result.is_some() is False
    assert result.is_none() is True
    with pytest.raises(AssertionError):
        assert result.unwrap() is not None

def test_some_class():
    """Test the Some class directly."""
    value = Some(42)
    assert value.is_some() is True
    assert value.is_none() is False
    assert value.unwrap() == 42

def test_none_type_class():
    """Test the NoneType class directly."""
    value = NoneType
    assert value.is_some() is False
    assert value.is_none() is True
    with pytest.raises(AssertionError):
        assert value.unwrap() is not None

def test_uadd_edge_case_zero():
    """Test the uadd function with edge case zero."""
    result = uadd(0, 0)
    assert isinstance(result, Some)
    assert result.is_some() is True
    assert result.is_none() is False
    assert result.unwrap() == 0

def test_error_handling():
    """Test NoneTypeException being raised."""
    result = uadd(-1, -1)
    assert result is NoneType
    with pytest.raises(AssertionError, match="value could not be None"):
        if result.is_none():
            raise AssertionError("value could not be None")

