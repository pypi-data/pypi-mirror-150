from typing import TypeVar

from py_desc.base import Base

T = TypeVar('T', bound=str)
C = TypeVar('C')


class String(Base):

    def __get__(self, instance: 'String', owner: C) -> T:
        return getattr(instance, self.name)

    def __set__(self, instance: 'String', value: T) -> None:
        if not isinstance(value, str):
            raise ValueError('Must be string')
        setattr(instance, self.name, value)

    def __set_name__(self, owner: C, name: str) -> None:
        self.name = f'_{name.lower()}'
