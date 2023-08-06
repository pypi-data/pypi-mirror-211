from __future__ import annotations

from abc import abstractmethod
from collections.abc import Iterable, Mapping
from typing import Optional, TypeVar, Union

from .base_hierarchy import BaseHierarchyBound
from .hierarchy_coordinates import HierarchyCoordinates
from .hierarchy_key import HierarchyKey
from .repr_json import ReprJson, ReprJsonable

HierarchyT = TypeVar("HierarchyT", bound=BaseHierarchyBound, covariant=True)


class BaseHierarchies(Mapping[tuple[str, str], HierarchyT], ReprJsonable):
    """Manage the base hierarchies."""

    @abstractmethod
    def __getitem__(self, key: HierarchyKey, /) -> HierarchyT:
        """Return the hierarchy with the given name."""

    def _repr_json_(self) -> ReprJson:
        """Return the JSON representation of hierarchies."""
        dimensions: dict[str, list[HierarchyT]] = {}
        for hierarchy in self.values():
            dimensions.setdefault(hierarchy.dimension, []).append(hierarchy)
        json = {
            dimension: dict(
                sorted(
                    {
                        hierarchy._repr_json_()[1]["root"]: hierarchy._repr_json_()[0]
                        for hierarchy in dimension_hierarchies
                    }.items()
                )
            )
            for dimension, dimension_hierarchies in sorted(dimensions.items())
        }
        return json, {"expanded": True, "root": "Dimensions"}

    @staticmethod
    def _convert_key(key: HierarchyKey, /) -> tuple[Optional[str], str]:
        """Get the dimension and hierarchy from the key."""
        if isinstance(key, str):
            return (None, key)

        return key

    @staticmethod
    def _multiple_hierarchies_error(
        key: HierarchyKey,
        hierarchies: Union[Iterable[HierarchyT], Iterable[HierarchyCoordinates]],
    ) -> KeyError:
        return KeyError(
            f"""Multiple hierarchies with name {key}. Specify the dimension: {", ".join([
            f'cube.hierarchies["{hierarchy.dimension_name}", "{hierarchy.dimension_name}"]'if isinstance(hierarchy, HierarchyCoordinates) else f'cube.hierarchies["{hierarchy.dimension}", "{hierarchy.name}"]'
            for hierarchy in hierarchies
        ])}"""
        )


BaseHierarchiesBound = BaseHierarchies[BaseHierarchyBound]
