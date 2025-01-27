from __future__ import annotations
from typing import Protocol, TypeVar, Generic, Optional, Iterator

T = TypeVar("T", covariant=True)


class Option(Protocol[T]):
    """
    Represents an optional value, inspired by Rust's `Option` type.
    An `Option` can either contain a value (`Some`) or represent the absence of a value (`NoneType`).

    This is useful for cases where a return value may or may not be present, avoiding the need for `None` directly.

    Example Usage:
        ```
        def safe_divide(x: int, y: int) -> Option[float]:
            if y == 0:
                return NoneType
            else:
                return Some(x / y)

        result = safe_divide(10, 2)
        if result.is_some():
            print(f"Result: {result.unwrap()}")
        else:
            print("Division by zero")
        ```
    """

    def is_some(self) -> bool:
        """
        Checks if the `Option` contains a value (`Some`).

        Returns:
            bool: `True` if the `Option` contains a value, otherwise `False`.

        Example:
            ```
            result = Some(42)
            print(result.is_some())  # True

            empty = NoneType()
            print(empty.is_some())  # False
            ```
        """
        ...

    def is_none(self) -> bool:
        """
        Checks if the `Option` represents the absence of a value (`NoneType`).

        Returns:
            bool: `True` if the `Option` is `NoneType`, otherwise `False`.

        Example:
            ```
            empty = NoneType
            print(empty.is_none())  # True

            result = Some(42)
            print(result.is_none())  # False
            ```
        """
        ...

    def unwrap(self) -> Optional[T]:
        """
        Extracts the value contained in the `Option`, if present.

        If the `Option` is `NoneType`, this method raises an exception to indicate that there is no value to unwrap.

        Returns:
            Optional[T]: The value contained in the `Option`, or `None` if it's `NoneType`.

        Raises:
            NoneTypeException: If the `Option` is `NoneType`.

        Example:
            ```
            result = Some(42)
            print(result.unwrap())  # 42

            empty = NoneType()
            print(empty.unwrap())  # Raises NoneTypeException
            ```
        """
        ...


class Some(Generic[T]):

    __match_args__ = ("value",)
    __slots__ = ("_value",)

    def __init__(self, value: T):
        self._value = value

    @property
    def value(self):
        return self._value

    def is_some(self) -> bool:
        """
        Return Literal True
        """
        return True

    def is_none(self) -> bool:
        """
        Return Literal False
        """
        return False

    def unwrap(self) -> Optional[T]:
        """
        Return Inner value
        """
        return self._value

    def __iter__(self) -> Iterator[T]:
        yield self._value

    def __repr__(self) -> str:
        return f"Some({str(self._value)})"

    def __str__(self) -> str:
        return f"Some({str(self._value)})"

    def __hash__(self):
        return hash((True, self._value))


class _NoneType:

    __match_args__ = ()
    __slots__ = ()
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def is_some(self) -> bool:
        """
        Return boolean if Some
        """
        return False

    def is_none(self) -> bool:
        """
        Return boolean if None
        """
        return True

    def unwrap(self) -> Optional[T]:
        """
        Return None
        """
        return None

    def __iter__(self) -> Iterator[None]:
        yield None

    def __repr__(self) -> str:
        return "None"

    def __str__(self) -> str:
        return "None"

    def __eq__(self, other) -> bool:
        """
        Act like `None` when compared
        """
        return other is None or other is self

    def __bool__(self) -> bool:
        """
        Mimic the falsy behavior of `None`
        """
        return False


NoneType = _NoneType()
