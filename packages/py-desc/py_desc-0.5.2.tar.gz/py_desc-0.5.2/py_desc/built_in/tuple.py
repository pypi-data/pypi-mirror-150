from typing import TypeVar

from py_desc.base import Base

T = TypeVar('T', bound=tuple)
C = TypeVar('C')


class SimpleTuple(Base):

    def __get__(self, instance: 'SimpleTuple', owner: C) -> T:
        return getattr(instance, self.name)

    def __set__(self, instance: 'SimpleTuple', value: T) -> None:
        if not isinstance(value, tuple):
            raise ValueError('Must be tuple')
        setattr(instance, self.name, value)

    def __set_name__(self, owner: C, name: str) -> None:
        self.name = f'_{name.lower()}'


class TupleOfIntegers(Base):

    def __get__(self, instance: 'TupleOfIntegers', owner: C) -> T:
        return getattr(instance, self.name)

    def __set__(self, instance: 'TupleOfIntegers', value: T) -> None:
        if not isinstance(value, tuple):
            raise ValueError('Must be tuple')
        if not all([isinstance(x, int) for x in value]):
            raise ValueError('Values in tuple must be integers')
        setattr(instance, self.name, value)

    def __set_name__(self, owner: C, name: str) -> None:
        self.name = f'_{name.lower()}'


class TupleOfFloats(Base):

    def __get__(self, instance: 'TupleOfFloats', owner: C) -> T:
        return getattr(instance, self.name)

    def __set__(self, instance: 'TupleOfFloats', value: T) -> None:
        if not isinstance(value, tuple):
            raise ValueError('Must be tuple')
        if not all([isinstance(x, float) for x in value]):
            raise ValueError('Values in tuple must be float')
        setattr(instance, self.name, value)

    def __set_name__(self, owner: C, name: str) -> None:
        self.name = f'_{name.lower()}'


class TupleOfNumbers(Base):

    def __get__(self, instance: 'TupleOfNumbers', owner: C) -> T:
        return getattr(instance, self.name)

    def __set__(self, instance: 'TupleOfNumbers', value: T) -> None:
        if not isinstance(value, tuple):
            raise ValueError('Must be tuple')
        if not all([isinstance(x, (int, float)) for x in value]):
            raise ValueError('Values in tuple must be integers or float')
        setattr(instance, self.name, value)

    def __set_name__(self, owner: C, name: str) -> None:
        self.name = f'_{name.lower()}'


class TupleOfStrings(Base):

    def __get__(self, instance: 'TupleOfStrings', owner: C) -> T:
        return getattr(instance, self.name)

    def __set__(self, instance: 'TupleOfStrings', value: T) -> None:
        if not isinstance(value, tuple):
            raise ValueError('Must be tuple')
        if not all([isinstance(x, str) for x in value]):
            raise ValueError('Values in tuple must be strings')
        setattr(instance, self.name, value)

    def __set_name__(self, owner: C, name: str) -> None:
        self.name = f'_{name.lower()}'


class CustomTuple(Base):

    def __init__(self, classinfo: type) -> None:
        self.classinfo = classinfo

    def __get__(self, instance: 'CustomTuple', owner: C) -> T:
        return getattr(instance, self.name)

    def __set__(self, instance: 'CustomTuple', value: T) -> None:
        if not isinstance(value, tuple):
            raise ValueError('Must be tuple')
        if not all([isinstance(x, self.classinfo) for x in value]):
            raise ValueError(f'Values in tuple must be {self.classinfo}')
        setattr(instance, self.name, value)

    def __set_name__(self, owner: C, name: str) -> None:
        self.name = f'_{name.lower()}'
