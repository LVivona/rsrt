import pytest
from rsrt import Result, Ok, Err, UnwrapError

def add(x : int ,y : int) -> Result[Ok[int], Err[BaseException]]:
    return Ok(x + y)

def uadd(x : int, y : int) -> Result[Ok[int],Err[AssertionError]]:
    try:
        assert x >= 0 and y >= 0, "x and y should be less then 0"
        return Ok(x + y)
    except AssertionError as e:
        return Err(e)

def test_add():
    """Test the add function with valid inputs."""
    result = add(2, 3)
    assert result.is_ok() is True
    assert result.is_err() is False
    assert result.unwrap() == 5

def test_uadd_positive_numbers():
    """Test the uadd function with valid inputs."""
    result = uadd(3, 4)
    assert isinstance(result, (Ok, Err))
    assert result.is_ok() is True
    assert result.is_err() is False
    assert result.unwrap() == 7

def test_uadd_negative_numbers():
    """Test the uadd function with invalid inputs."""
    result = uadd(-1, 4)
    print(result)
    assert result.is_ok() is False
    assert result.is_err() is True
    with pytest.raises(UnwrapError, match="x and y should be less then 0"):
        result.unwrap()

def test_some_class():
    """Test the Some class directly."""
    value = Ok(42)
    assert value.is_ok() is True
    assert value.is_err() is False
    assert value.unwrap() == 42

def test_positive_match_case():
    result = add(41, 1)
    match result:
        case Ok(value):
            assert value == 42
        case Err(error):
            print(f"Exception received: {error}")

def test_negative_match_case():
    result = uadd(42, -1)
    match result:
        case Ok(_):
            raise Exception
        case Err(error):
            assert isinstance(error, AssertionError)
