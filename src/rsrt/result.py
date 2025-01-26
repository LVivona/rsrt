"""
This file rust.py is based on the `rustedpy/result` library:
https://github.com/rustedpy/result

the implementation within rustepy was used to suit the needs of this project.
"""
from __future__ import annotations
import sys
from typing import (TypeVar, 
                    Generic, 
                    Any, 
                    Iterator, 
                    Union, 
                    Final, 
                    Optional,
                    Callable,
                    Awaitable)
from .errors import UnwrapError, DoException

if sys.version_info > (3, 10):
    from typing import TypeAlias, ParamSpec
else:
    from typing_extensions import TypeAlias, ParamSpec

T = TypeVar("T", covariant=True) # Success type
E = TypeVar("E", covariant=True) # Error type
U = TypeVar("U")
F = TypeVar("F")
P = ParamSpec("P")
R = TypeVar("R")



class Ok(Generic[T]):
    __match_args__ = ("value",)
    __slots__ = ("_value", )

    def __init__(self, value : T):
        self._value = value

    def is_err(self) -> bool:
        """
        Return boolean False
        """
        return False
    
    def is_ok(self) -> bool:
        """
        Return boolean True
        """
        return True

    def unwrap(self) -> T:
        """
        Return the value
        """
        return self._value    
    
    def ok(self) -> T:
        """
        Return the value.
        """
        return self._value

    def err(self) -> None:
        """
        Return `None`.
        """
        return None

    def expect(self, message : Optional[str]):
        """
            Return the value
        """
        return self._value
    
    def expect_err(self, message : Optional[str]):
        return UnwrapError(self, message)

    def unwrap_err(self) -> None:
        """
        Raise an UnwrapError since this type is `Ok`
        """
        raise UnwrapError(self, "Called `Result.unwrap_err()` on an `Ok` value")
    
    def unwrap_or_else(self, op: Callable[[E], T]) -> T:
        """
        The contained result is ``Err``, so return the result of applying
        ``op`` to the error value.
        """
        return self._value
    
    def unwrap_or(self, default: U) -> U:
        """
        Return value.
        """
        return self._value
    
    def and_then(self, op: Callable[[T], Result[U, E]]) -> Result[U, E]:
        """
        The contained result is `Ok`, so return the result of `op` with the
        original value passed in
        """
        return op(self._value)

    async def and_then_async(
        self, op: Callable[[T], Awaitable[Result[U, E]]]
    ) -> Result[U, E]:
        """
        The contained result is `Ok`, so return the result of `op` with the
        original value passed in
        """
        return await op(self._value)

    def or_else(self, op: object) -> Ok[T]:
        """
        The contained result is `Ok`, so return `Ok` with the original value
        """
        return self

    def inspect(self, op: Callable[[T], Any]) -> Result[T, E]:
        """
        Calls a function with the contained value if `Ok`. Returns the original result.
        """
        op(self._value)
        return self

    def inspect_err(self, op: Callable[[E], Any]) -> Result[T, E]:
        """
        Calls a function with the contained value if `Err`. Returns the original result.
        """
        return self
    
    @property
    def value(self) -> T:
        """
        Return inner value used for match statements
        """
        return self._value
    
    def __repr__(self):
        return f"Ok({self._value})"
    
    def __eq__(self, other : Any):
        return isinstance(other, Ok) and self._value == other._value

    def __ne__(self, other: Any) -> bool:
        return not (self == other)

    def __hash__(self) -> int:
        return hash((True, self._value))


class Err(Generic[E]):
    
    __match_args__ = ("error",)
    __slots__ = ("_value", )

    def __init__(self, value : E):
        self._value = value
    
    def is_err(self) -> bool:
        return True
    
    def is_ok(self) -> bool:
        return False
    
    def unwrap(self) -> None:
        """
        Raises an `UnwrapError`.
        """
        exc = UnwrapError(
            self,
            f"Called `Result.unwrap()` on an `Err` value: {self._value!r}",
        )
        if isinstance(self._value, BaseException):
            raise exc from self._value
        raise exc

    def ok(self) -> T:
        """
        Return `None`.
        """
        return None

    def err(self) -> None:
        """
        raise exception 
        """
        exc = UnwrapError(
            self,
            f"Called `Result.unwrap()` on an `Err` value: {self._value!r}",
        )
        if isinstance(self._value, BaseException):
            raise exc from self._value
        raise exc
    
    def expect(self, message: str) -> None:
        """
        Raises an `UnwrapError`.
        """
        exc = UnwrapError(
            self,
            f"{message}: {self._value!r}",
        )
        if isinstance(self._value, BaseException):
            raise exc from self._value
        raise exc

    def expect_err(self, _message: str) -> E:
        """
        Return the inner value
        """
        return self._value
    
    def unwrap_or(self, default: U) -> U:
        """
        Return `default`.
        """
        return default
    
    def unwrap_or_else(self, op: Callable[[E], T]) -> T:
        """
        The contained result is ``Err``, so return the result of applying
        ``op`` to the error value.
        """
        return op(self._value)
    
    def and_then(self, op: object) -> Err[E]:
        """
        The contained result is `Err`, so return `Err` with the original value
        """
        return self

    async def and_then_async(self, op: object) -> Err[E]:
        """
        The contained result is `Err`, so return `Err` with the original value
        """
        return self

    def or_else(self, op: Callable[[E], Result[T, F]]) -> Result[T, F]:
        """
        The contained result is `Err`, so return the result of `op` with the
        original value passed in
        """
        return op(self._value)
    
    def inspect(self, op: Callable[[T], Any]) -> Result[T, E]:
        """
        Calls a function with the contained value if `Ok`. Returns the original result.
        """
        return self

    def inspect_err(self, op: Callable[[E], Any]) -> Result[T, E]:
        """
        Calls a function with the contained value if `Err`. Returns the original result.
        """
        op(self._value)
        return self
    
    @property
    def error(self):
        return self._value
    
    def __iter__(self):
         yield self._value
    
    def __repr__(self):
        return f"Err({self._value})"
    
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Err) and self._value == other._value

    def __hash__(self) -> int:
        return hash((False, self._value))
    
    def __iter__(self) -> Iterator[None]:
        def _iter() -> Iterator[None]:
            # Exception will be raised when the iterator is advanced, not when it's created
            raise DoException(self)
            yield  # This yield will never be reached, but is necessary to create a generator

        return _iter()

"""
A simple `Result` type inspired by Rust.
Not all methods (https://doc.rust-lang.org/std/result/enum.Result.html)
have been implemented, only the ones that make sense in the Python context.
"""
Result : TypeAlias = Union[Ok[T], Err[E]]

"""
A type to use in `isinstance` checks.
This is purely for convenience sake, as you could also just write `isinstance(res, (Ok, Err))
"""
OkErr: Final = (Ok, Err)