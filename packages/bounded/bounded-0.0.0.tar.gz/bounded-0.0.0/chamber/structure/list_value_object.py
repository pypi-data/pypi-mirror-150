from typing import Type, Any, TypeVar, List, Union
from abc import abstractmethod
from pydantic import BaseModel

from chamber.base import Serializable


T = TypeVar('T')


def _validate(item: Any, type_: Type[T]) -> T:
    if isinstance(item, type_):
        return item
    if issubclass(type_, BaseModel):
        if isinstance(item, dict):
            return type_(**item)
    try:
        return type_(item)
    except:
        raise TypeError('Type Validation Error')


def _serialize(d):
    if isinstance(d, Serializable):
        return d.serialize()
    return d


class ListValueObject(BaseModel, Serializable):
    _data: list

    @property
    @abstractmethod
    def item_type(self) -> Type[Any]:
        pass

    def __init__(self, *items):
        super().__init__()

        self._data = [_validate(item, self.item_type) for item in items]

    def serialize(self) -> List:
        return [_serialize(d) for d in self._data]

    @classmethod
    def deserialize(cls, obj: dict) -> 'ListValueObject':
        return cls(*obj)

    def __iter__(self):
        yield from self._data

    def __eq__(self, other):
        if self.__class__ is not other.__class__:
            return False
        return all([s == o for s, o in zip(self._data, other._data)])

    def __hash__(self):
        return tuple(self._data).__hash__()

    def __repr__(self):
        if len(self._data) > 3:
            data_sample = ', '.join(map(repr, [self._data[0], self._data[1], '...', self._data[-1]]))
        else:
            data_sample = ', '.join(map(repr, self._data))

        return f'{self.__class__.__name__}({data_sample})'

    def __add__(self, other: Union['ListValueObject', List]):
        if other.__class__ is self.__class__:
            return self.__class__(*(self._data + other._data))
        raise TypeError('ListValueObject addition of different types is not allowed')

    class Config:
        extra = 'forbid'
        allow_mutation = False
        underscore_attrs_are_private = True
