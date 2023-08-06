from __future__ import annotations

from abc import abstractmethod
from collections.abc import (
    ItemsView,
    Iterable,
    Iterator,
    KeysView,
    Mapping,
    MutableMapping,
    ValuesView,
)
from typing import (
    TYPE_CHECKING,
    Optional,
    TypeVar,
    Union,
    overload,
)

from .ipython_key_completions import (
    IPythonKeyCompletions,
    get_ipython_key_completions_for_mapping,
)

if TYPE_CHECKING:
    from _typeshed import SupportsKeysAndGetItem  # pylint: disable=nested-import

_Key = TypeVar("_Key")
_Value = TypeVar("_Value")


class DelegateMutableMapping(MutableMapping[_Key, _Value]):
    # `keys()`, `items()`, and `values()` methods are reimplemented for performance reasons.
    # See https://github.com/activeviam/atoti-python-api/pull/1162#issuecomment-592551497.

    @abstractmethod
    def _get_underlying(self) -> dict[_Key, _Value]:
        ...

    @abstractmethod
    def _update(self, other: Mapping[_Key, _Value], /) -> None:
        ...

    @abstractmethod
    def _delete_keys(self, keys: Optional[Iterable[_Key]] = None, /) -> None:
        ...

    def __delitem__(self, key: _Key, /) -> None:
        return self._delete_keys([key])

    def clear(self) -> None:
        return self._delete_keys()

    @overload
    def update(
        self, __m: SupportsKeysAndGetItem[_Key, _Value], **kwargs: _Value
    ) -> None:
        ...

    @overload
    def update(self, __m: Iterable[tuple[_Key, _Value]], **kwargs: _Value) -> None:
        ...

    @overload
    def update(self, **kwargs: _Value) -> None:
        ...

    # Pyright fails to see that the override is correct but mypy can see it.
    def update(  # type: ignore[misc] # pyright: ignore[reportGeneralTypeIssues]
        self,
        __m: Optional[
            Union[Mapping[_Key, _Value], Iterable[tuple[_Key, _Value]]]
        ] = None,
        **kwargs: _Value,
    ) -> None:
        """Update the mapping.

        :meta private:
        """
        other: dict[_Key, _Value] = {}
        if __m is not None:
            other.update(__m)
        other.update(**kwargs)
        self._update(other)

    def __setitem__(self, key: _Key, value: _Value, /) -> None:
        self.update({key: value})

    def __getitem__(self, key: _Key, /) -> _Value:
        return self._get_underlying()[key]

    def __iter__(self) -> Iterator[_Key]:
        return iter(self._get_underlying())

    def __len__(self) -> int:
        return len(self._get_underlying())

    def __repr__(self) -> str:
        return repr(self._get_underlying())

    def keys(self) -> KeysView[_Key]:
        return self._get_underlying().keys()

    def items(self) -> ItemsView[_Key, _Value]:
        return self._get_underlying().items()

    def values(self) -> ValuesView[_Value]:
        return self._get_underlying().values()

    def _ipython_key_completions_(self) -> IPythonKeyCompletions:
        return get_ipython_key_completions_for_mapping(self)  # type: ignore[arg-type] # pyright: ignore[reportGeneralTypeIssues]

    def _default_to_all_keys(
        self, keys: Optional[Iterable[_Key]] = None, /
    ) -> Iterable[_Key]:
        return self.keys() if keys is None else keys
