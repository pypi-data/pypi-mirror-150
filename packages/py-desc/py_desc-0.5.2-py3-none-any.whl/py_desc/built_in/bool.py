from typing import TypeVar

from py_desc.base import Base

T = TypeVar('T', bound=bool)
C = TypeVar('C')


class Boolean(Base):

    def __get__(self, instance: 'Boolean', owner: C) -> T:
        return getattr(instance, self.name)

    def __set__(self, instance: 'Boolean', value: T) -> None:
        if not isinstance(value, bool):
            raise ValueError('Must be boolean')
        setattr(instance, self.name, value)

    def __set_name__(self, owner: C, name: str) -> None:
        self.name = f'_{name.lower()}'


class TrueBoolean(Base):

    def __get__(self, instance: 'TrueBoolean', owner: C) -> T:
        return getattr(instance, self.name)

    def __set__(self, instance: 'TrueBoolean', value: T) -> None:
        if not isinstance(value, bool):
            raise ValueError('Must be boolean')
        if not value:
            raise ValueError('Cannot be True')
        setattr(instance, self.name, value)

    def __set_name__(self, owner: C, name: str) -> None:
        self.name = f'_{name.lower()}'


class FalseBoolean(Base):

    def __get__(self, instance: 'FalseBoolean', owner: C) -> T:
        return getattr(instance, self.name)

    def __set__(self, instance: 'FalseBoolean', value: T) -> None:
        if not isinstance(value, bool):
            raise ValueError('Must be boolean')
        if value:
            raise ValueError('Cannot be True')
        setattr(instance, self.name, value)

    def __set_name__(self, owner: C, name: str) -> None:
        self.name = f'_{name.lower()}'
