from pydantic import BaseModel

from chamber.base import Serializable


class ValueObject(BaseModel, Serializable):
    class Config:
        allow_mutation = False
        extra = 'forbid'

    def serialize(self):
        return self.dict()

    @classmethod
    def deserialize(cls, obj: dict) -> 'ValueObject':
        return cls(**obj)

    def __eq__(self, other):
        if self.__class__ is not other.__class__:
            return False
        return super().__eq__(other)
