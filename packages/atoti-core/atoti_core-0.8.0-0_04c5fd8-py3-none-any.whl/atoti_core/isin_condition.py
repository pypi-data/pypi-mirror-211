from collections.abc import Iterable
from dataclasses import dataclass
from functools import cached_property
from typing import Literal, Optional, TypeVar

from .combine_conditions import combine_conditions
from .constant import Constant
from .coordinates import Coordinates
from .hierarchy_coordinates import HierarchyCoordinates
from .operation import (
    ComparisonCondition,
    Condition,
    ConditionCombinationOperatorBound,
    ConditionComparisonOperatorBound,
    ConditionSubjectT,
)

IsinConditionElementT = TypeVar(
    "IsinConditionElementT", bound=Optional[Constant], covariant=True
)


@dataclass(frozen=True)
class IsinCondition(
    Condition[ConditionSubjectT, Literal["isin"], IsinConditionElementT, None]
):
    subject: ConditionSubjectT
    _elements: frozenset[IsinConditionElementT]

    def __init__(
        self, *, subject: ConditionSubjectT, elements: Iterable[IsinConditionElementT]
    ) -> None:
        assert not isinstance(
            subject, HierarchyCoordinates
        ), "Conditions on hierarchies must use `HierarchyIsinCondition`."

        if not elements:
            raise ValueError(
                "No passed elements, the condition will always evaluate to `False`."
            )

        self.__dict__["subject"] = subject
        self.__dict__["_elements"] = frozenset(elements)

    @cached_property
    def elements(self) -> tuple[IsinConditionElementT, ...]:
        # The elements are sorted to ensure predictability.
        return (
            # Collections containing `None` cannot be sorted.
            # If `None` is in the elements it's added at the head of the tuple.
            # The remaining non-`None` elements are sorted and inserted after.
            *([None] if None in self._elements else []),  # type: ignore[arg-type] # pyright: ignore[reportGeneralTypeIssues]
            *sorted(element for element in self._elements if element is not None),  # type: ignore[type-var]
        )

    @cached_property
    def normalized(
        self,
    ) -> Condition[
        ConditionSubjectT, Literal["eq", "isin"], IsinConditionElementT, None
    ]:
        if len(self.elements) != 1:
            return self

        return ComparisonCondition(
            subject=self.subject, operator="eq", target=self.elements[0]
        )

    @property
    def combined_comparison_condition(
        self,
    ) -> Condition[
        ConditionSubjectT, Literal["eq"], IsinConditionElementT, Optional[Literal["or"]]
    ]:
        return combine_conditions(
            [
                (
                    ComparisonCondition(
                        subject=self.subject, operator="eq", target=element
                    ),
                )
                for element in self.elements
            ]
        )

    @property
    def _coordinates_classes(self) -> frozenset[type[Coordinates]]:
        return self._get_coordinates_classes(self.subject)

    def __invert__(
        self,
    ) -> Condition[
        ConditionSubjectT,
        ConditionComparisonOperatorBound,
        IsinConditionElementT,
        ConditionCombinationOperatorBound,
    ]:
        return ~self.combined_comparison_condition

    def __repr__(self) -> str:
        return f"{self.subject!r}.isin{tuple(element.value if isinstance(element, Constant) else element for element in self.elements)!r}"


IsinConditionBound = IsinCondition[Coordinates, Optional[Constant]]
