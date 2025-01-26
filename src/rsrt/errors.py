from __future__ import annotations
import sys
from typing import Any, TypeVar

if sys.version_info > (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

class UnwrapError(Exception):
    """
    github: https://github.com/rustedpy/result/blob/main/src/result/result.py

    Exception raised from ``.unwrap_<...>`` and ``.expect_<...>`` calls.

    The original ``Result`` can be accessed via the ``.result`` attribute, but
    this is not intended for regular use, as type information is lost:
    ``UnwrapError`` doesn't know about both ``T`` and ``E``, since it's raised
    from ``Ok()`` or ``Err()`` which only knows about either ``T`` or ``E``,
    not both.
    """

    _result: "Result[object, object]"

    def __init__(self, result: "Result[object, object]", message: str) -> None:
        self._result = result
        super().__init__(message)

    @property
    def result(self) -> "Result[Any, Any]":
        """
        Returns the original result.
        """
        return self._result
    
class DoException(Exception):
    """
    github: https://github.com/rustedpy/result/blob/main/src/result/result.py

    This is used to signal to `do()` that the result is an `Err`,
    which short-circuits the generator and returns that Err.
    Using this exception for control flow in `do()` allows us
    to simulate `and_then()` in the Err case: namely, we don't call `op`,
    we just return `self` (the Err).
    """

    def __init__(self, err: "Err[E]") -> None:
        self.err = err

