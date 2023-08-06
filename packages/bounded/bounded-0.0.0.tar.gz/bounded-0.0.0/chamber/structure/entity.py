from typing import TypeVar, Type
from pydantic import BaseModel
from chamber.base import Serializable


ImplType = TypeVar('ImplType')


class Entity(BaseModel, Serializable):
    class Config:
        extra = 'forbid'

    def serialize(self):
        return self.dict()

    @classmethod
    def deserialize(cls: Type[ImplType], obj: dict) -> ImplType:
        return cls(**obj)
