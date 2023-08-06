from typing import TypeVar

from py_desc.base import Base

T = TypeVar('T', bound=set)
C = TypeVar('C')


class SimpleSet(Base):

    def __get__(self, instance: 'SimpleSet', owner: C) -> T:
        return getattr(instance, self.name)

    def __set__(self, instance: 'SimpleSet', value: T) -> None:
        if not isinstance(value, set):
            raise ValueError('Must be set')
        setattr(instance, self.name, value)

    def __set_name__(self, owner: C, name: str) -> None:
        self.name = f'_{name.lower()}'


class SetOfIntegers(Base):

    def __get__(self, instance: 'SetOfIntegers', owner: C) -> T:
        return getattr(instance, self.name)

    def __set__(self, instance: 'SetOfIntegers', value: T) -> None:
        if not isinstance(value, set):
            raise ValueError('Must be set')
        if not all([isinstance(x, int) for x in value]):
            raise ValueError('Values in set must be integers')
        setattr(instance, self.name, value)

    def __set_name__(self, owner: C, name: str) -> None:
        self.name = f'_{name.lower()}'


class SetOfFloats(Base):

    def __get__(self, instance: 'SetOfFloats', owner: C) -> T:
        return getattr(instance, self.name)

    def __set__(self, instance: 'SetOfFloats', value: T) -> None:
        if not isinstance(value, set):
            raise ValueError('Must be set')
        if not all([isinstance(x, float) for x in value]):
            raise ValueError('Values in set must be float')
        setattr(instance, self.name, value)

    def __set_name__(self, owner: C, name: str) -> None:
        self.name = f'_{name.lower()}'


class SetOfNumbers(Base):

    def __get__(self, instance: 'SetOfNumbers', owner: C) -> T:
        return getattr(instance, self.name)

    def __set__(self, instance: 'SetOfNumbers', value: T) -> None:
        if not isinstance(value, set):
            raise ValueError('Must be set')
        if not all([isinstance(x, (int, float)) for x in value]):
            raise ValueError('Values in set must be integers or float')
        setattr(instance, self.name, value)

    def __set_name__(self, owner: C, name: str) -> None:
        self.name = f'_{name.lower()}'


class SetOfStrings(Base):

    def __get__(self, instance: 'SetOfStrings', owner: C) -> T:
        return getattr(instance, self.name)

    def __set__(self, instance: 'SetOfStrings', value: T) -> None:
        if not isinstance(value, set):
            raise ValueError('Must be set')
        if not all([isinstance(x, str) for x in value]):
            raise ValueError('Values in set must be strings')
        setattr(instance, self.name, value)

    def __set_name__(self, owner: C, name: str) -> None:
        self.name = f'_{name.lower()}'


class CustomSet(Base):

    def __init__(self, classinfo: type) -> None:
        self.classinfo = classinfo

    def __get__(self, instance: 'CustomSet', owner: C) -> T:
        return getattr(instance, self.name)

    def __set__(self, instance: 'CustomSet', value: T) -> None:
        if not isinstance(value, set):
            raise ValueError('Must be set')
        if not all([isinstance(x, self.classinfo) for x in value]):
            raise ValueError(f'Values in set must be {self.classinfo}')
        setattr(instance, self.name, value)

    def __set_name__(self, owner: C, name: str) -> None:
        self.name = f'_{name.lower()}'
