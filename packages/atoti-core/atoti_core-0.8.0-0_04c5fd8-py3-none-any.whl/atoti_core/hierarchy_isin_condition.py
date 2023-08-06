from collections.abc import Iterable
from dataclasses import dataclass
from functools import cached_property
from typing import Literal, NoReturn, Optional, Union

from .combine_conditions import combine_conditions
from .constant import Constant
from .coordinates import Coordinates
from .hierarchy_coordinates import HierarchyCoordinates
from .level_coordinates import LevelCoordinates
from .operation import ComparisonCondition, Condition, ConditionCombinationOperatorBound


@dataclass(frozen=True)
class HierarchyIsinCondition(
    Condition[HierarchyCoordinates, Literal["isin"], Constant, None]
):
    subject: HierarchyCoordinates
    level_names: tuple[str, ...]
    _member_paths: frozenset[tuple[Constant, ...]]

    def __init__(
        self,
        *,
        subject: HierarchyCoordinates,
        level_names: tuple[str, ...],
        member_paths: Iterable[tuple[Constant, ...]],
    ) -> None:
        if not member_paths:
            raise ValueError(
                "No passed member paths, the condition will always evaluate to `False`."
            )

        for member_path in member_paths:
            if not member_path:
                raise ValueError(
                    "Passed one empty member path: it is unnecessary since it will always evaluate to `False`."
                )

            if len(member_path) > len(level_names):
                raise ValueError(
                    f"Member path `{tuple(member.value for member in member_path)}` contains more than {len(level_names)} elements which is the number of levels of `{subject!r}`."
                )

        self.__dict__["subject"] = subject
        self.__dict__["level_names"] = level_names
        self.__dict__["_member_paths"] = frozenset(member_paths)

    @cached_property
    def member_paths(self) -> tuple[tuple[Constant, ...], ...]:
        # The member paths are sorted to ensure predictability.
        return tuple(sorted(self._member_paths))

    @cached_property
    def normalized(
        self,
    ) -> Condition[
        Union[HierarchyCoordinates, LevelCoordinates],
        Literal["eq", "isin"],
        Constant,
        Optional[Literal["and"]],
    ]:
        if len(self.member_paths) != 1:
            return self

        return combine_conditions(
            (
                [
                    ComparisonCondition(
                        subject=LevelCoordinates(
                            self.subject.dimension_name,
                            self.subject.hierarchy_name,
                            level_name,
                        ),
                        operator="eq",
                        target=member,
                    )
                    for level_name, member in zip(
                        self.level_names, next(iter(self.member_paths))
                    )
                ],
            )
        )

    @property
    def combined_comparison_condition(
        self,
    ) -> Condition[
        LevelCoordinates, Literal["eq"], Constant, ConditionCombinationOperatorBound
    ]:
        return combine_conditions(
            [
                [
                    ComparisonCondition(
                        subject=LevelCoordinates(
                            self.subject.dimension_name,
                            self.subject.hierarchy_name,
                            level_name,
                        ),
                        operator="eq",
                        target=member,
                    )
                    for level_name, member in zip(self.level_names, member_path)
                ]
                for member_path in self.member_paths
            ]
        )

    @property
    def _coordinates_classes(self) -> frozenset[type[Coordinates]]:
        return frozenset([type(self.subject)])

    def __invert__(
        self,
    ) -> NoReturn:
        raise RuntimeError(f"A `{type(self).__name__}` cannot be inverted.")
        # It can actually be done using `~hierarchy_isin_condition.combined_comparison_condition` but this changes the type of `subject` which breaks the contract of `Condition.__invert__()`.

    def __repr__(self) -> str:
        return f"{self.subject!r}.isin{tuple(tuple(member.value for member in member_path) for member_path in self.member_paths)!r}"
