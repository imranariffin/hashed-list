from typing import Callable, Dict, Optional, SupportsIndex, Iterable, List, Tuple, TypeVar, Union

T = TypeVar("T")


class DuplicateValueError(Exception):
    pass


class HashedList(List[T]):
    """
    A List with O(1) time complexity for `.index()` method, instead of O(N).

    A data structure that is pretty much a Python list, except that:
        1. The method `.index(value)` is O(1) (Good)
        2. The data structure uses twice more memory due to indexing
           (Not good but still okay)
        3. Items must be unique. It will raise DuplicateValueError if
           duplicate item is provided

    Main use case:
        You have a huge list of unique items that:
            1. You may update the list (remove, insert, set value etc) from
               time to time
            2. You may get the index of a specific item in the list from
               time to time

        In this case, using just a regular list definitely works but will cost
        you O(N) each time you get the index of a specific item. Or, you can
        maintain along the list a dictionary of item => index ,but that will cost
        you the burden of updating the dictionary everytime the list is updated.

        HashedList will make the work easy for you.
    """

    __slots__ = ("_index",)

    _index: Dict[T, int]

    def __init__(self, iterable: Iterable[T]):
        self._create_index(iterable=iterable)
        super().__init__(iterable)

    def __setitem__(self, key: Union[SupportsIndex, slice], value: Union[T, Iterable[T]]) -> None:
        new_values: Tuple[T] = tuple(value) if isinstance(value, Iterable) else (value,)
        old_values: Tuple[T] = tuple(self[key]) if isinstance(value, Iterable) else (self[key],)
        for new_value in new_values:
            self._validate_value(new_value)
        super().__setitem__(key, value)
        # Remove old indices
        for old_value in old_values:
            del self._index[old_value]
        # Update indices
        if isinstance(key, SupportsIndex):
            new_key_values = [(key, value)]
        else:  # key is a slice
            new_key_values = zip(range(key.start, key.stop), value)
        for new_index, new_value in new_key_values:
            self._index[new_value] = int(new_index)

    def __contains__(self, item: T):
        return item in self._index

    def append(self, value: T) -> None:
        self._validate_value(value)
        super().append(value)
        self._index[value] = len(self) - 1

    def extend(self, iterable: Iterable[T]) -> None:
        old_length = len(self)
        super().extend(iterable)
        for i, v in enumerate(iterable):
            self._validate_value(v)
            self._index[v] = old_length + i

    def insert(self, index: int, value: T) -> None:
        self._validate_value(value)
        super().insert(index, value)
        # Increment indices for the inserted value and all existing values to the right
        self._index[value] = index
        for i in range(index + 1, len(self)):
            self._index[self[i]] += 1

    def remove(self, value: T) -> None:
        super().remove(value)
        index = self._index[value]
        del self._index[value]
        # Decrement indices for all existing values to the right of the removed value
        for i in range(index, len(self)):
            self._index[self[i]] -= 1

    def pop(self, index: Optional[int] = None) -> T:
        value = super().pop(index) if index is not None else super().pop()
        if index is None:
            return value
        # Decrement indices for all existing values to the right of the removed value
        for i in range(index, len(self)):
            self._index[self[i]] -= 1
        return value

    def clear(self) -> None:
        super().clear()
        self._index = {}

    def index(self, value: T, start: Optional[int] = None, end: Optional[int] = None) -> int:
        try:
            index = self._index[value]
        except KeyError as error:
            raise ValueError(f"{value!r} is not in list") from error

        if start is not None and index < start or end is not None and index >= end:
            raise ValueError(f"{value!r} is not in list")

        return index

    def reverse(self) -> None:
        super().reverse()
        self._create_index(self)

    def sort(self, *, key: Optional[Callable] = None, reverse: bool = False) -> None:
        super().sort(key=key, reverse=reverse)
        self._create_index(iterable=self)

    def _validate_value(self, value: T) -> None:
        if value in self._index:
            raise DuplicateValueError(f"Duplicate values in HashedList")

    def _create_index(self, iterable: Iterable[T]) -> None:
        self._index = {}
        for i, v in enumerate(iterable):
            if v in self._index:
                raise DuplicateValueError(f"Duplicate values in HashedList")
            self._index[v] = i
