from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import date, datetime, time

# Here `get_args()` is used on `Union`, not on `Literal`.
from typing import (  # pylint: disable=preferred-function
    Any,
    NoReturn,
    Union,
    get_args,
)

from typing_extensions import TypeGuard

from .data_type import DataType

_ConstantArrayElement = Union[float, int]

ConstantValue = Union[
    bool,
    date,
    datetime,
    float,
    int,
    Iterable[_ConstantArrayElement],
    str,
    time,
]

_CONSTANT_ARRAY_ELEMENT_TYPES = get_args(_ConstantArrayElement)


def _get_checked_value_and_data_type(  # noqa: C901, PLR0911, PLR0912
    value: ConstantValue, /
) -> tuple[ConstantValue, DataType]:
    # Use the widest types to avoid compilation problems.
    # For better performance, types are checked from the most probable to the least.

    if isinstance(value, bool):
        return value, "boolean"
    if isinstance(value, float):
        if math.isnan(value):
            raise ValueError(
                f"`{value}` is not a valid constant value. To compare against NaN, use `isnan()` instead."
            )

        return value, "double"
    if isinstance(value, int):
        return value, "long"
    if isinstance(value, str):
        return value, "String"
    if isinstance(value, datetime):
        return value, "LocalDateTime" if value.tzinfo is None else "ZonedDateTime"
    if isinstance(value, date):
        return value, "LocalDate"
    if isinstance(value, time):
        return value, "LocalTime"
    if isinstance(value, tuple):
        # `tuple` is intentionally not supported so that branches of `Union[ConstantValue, Tuple[ConstantValue, ...]]` can be distinguised with an `isinstance(value, tuple)` check.
        # This is used for `switch()`'s `cases` parameter for instance.
        raise TypeError(
            "Tuples are not valid constant values. Use lists for constant arrays instead."
        )
    if isinstance(value, list):
        if len(value) == 0:
            raise ValueError(
                "Empty arrays are not supported as their data type cannot be inferred."
            )

        invalid_array_element_type = next(
            (
                type(element)
                for element in value
                if not isinstance(element, _CONSTANT_ARRAY_ELEMENT_TYPES)
            ),
            None,
        )

        if invalid_array_element_type:
            raise TypeError(
                f"Expected all the elements of the constant array to have a type of `{[valid_type.__name__ for valid_type in _CONSTANT_ARRAY_ELEMENT_TYPES]}` but got `{invalid_array_element_type.__name__}`."
            )

        # Lists are stored as tuples to ensure full immutability.
        if any(isinstance(element, float) for element in value):
            return tuple(float(element) for element in value), "double[]"

        return tuple(int(element) for element in value), "long[]"

    raise TypeError(f"Unexpected constant value type: `{type(value).__name__}`.")


def is_constant_value(value: Any, /) -> TypeGuard[ConstantValue]:
    try:
        Constant(value)
    except (TypeError, ValueError):
        return False
    else:
        return True


@dataclass(frozen=True)
class Constant:  # pylint: disable=keyword-only-dataclass
    data_type: DataType = field(init=False, compare=False, repr=False)
    value: ConstantValue

    def __post_init__(self) -> None:
        value, data_type = _get_checked_value_and_data_type(self.value)
        self.__dict__["data_type"] = data_type
        self.__dict__["value"] = value

    def __lt__(self, other: Any) -> bool:  # noqa: C901
        if not isinstance(other, Constant):
            raise TypeError(
                f"Cannot compare `{Constant.__name__}` to `{type(other).__name__}`."
            )

        def raise_type_error() -> NoReturn:
            raise TypeError(
                f"Cannot compare `{self.data_type}` `{Constant.__name__}` to `{other.data_type}` `{Constant.__name__}`."
            )

        if isinstance(self.value, (bool, int, float)):
            if not isinstance(other.value, (bool, int, float)):
                raise_type_error()
            return self.value < other.value

        if isinstance(self.value, str):
            if not isinstance(other.value, str):
                raise_type_error()
            return self.value < other.value

        if isinstance(self.value, Iterable):
            if not isinstance(other.value, Iterable):
                raise_type_error()
            return tuple(self.value) < tuple(other.value)

        if isinstance(self.value, date):
            if not isinstance(other.value, date):
                raise_type_error()
            return self.value < other.value

        if isinstance(self.value, datetime):
            if not isinstance(other.value, date):
                raise_type_error()
            return self.value < other.value

        # All the other types have already been handled.
        assert isinstance(self.value, time)

        if not isinstance(other.value, time):
            raise_type_error()
        return self.value < other.value
