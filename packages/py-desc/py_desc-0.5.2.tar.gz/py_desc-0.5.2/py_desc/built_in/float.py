from typing import Generic, Optional, TypeVar

from py_desc.base import Base

T = TypeVar('T', int, float)
V = TypeVar('V', bound=float)
C = TypeVar('C')


class PositiveFloat(Base):

    def __get__(self, instance: 'PositiveFloat', owner: C) -> V:
        return getattr(instance, self.name)

    def __set__(self, instance: 'PositiveFloat', value: V) -> None:
        if not isinstance(value, float):
            raise ValueError('Must be float')
        if value < 0:
            raise ValueError('Cannot be negative')
        setattr(instance, self.name, value)

    def __set_name__(self, owner: C, name: str) -> None:
        self.name = f'_{name.lower()}'


class NegativeFloat(Base):

    def __get__(self, instance: 'NegativeFloat', owner: C) -> V:
        return getattr(instance, self.name)

    def __set__(self, instance: 'NegativeFloat', value: V) -> None:
        if not isinstance(value, float):
            raise ValueError('Must be float')
        if value >= 0:
            raise ValueError('Cannot be positive')
        setattr(instance, self.name, value)

    def __set_name__(self, owner: C, name: str) -> None:
        self.name = f'_{name.lower()}'


class CustomFloat(Base, Generic[T]):

    def __init__(self, left: Optional[T] = None, right: Optional[T] = None) -> None:
        if not (isinstance(left, (int, float)) and isinstance(right, (int, float))):
            if left is not None and right is not None:
                raise AttributeError('Cannot assign parameters for float field')
        if left is not None and right is not None:
            if left > right:
                raise AttributeError('Cannot assign last_value smaller then first_value')

        self.left: Optional[T] = left
        self.right: Optional[T] = right

    def __get__(self, instance: 'CustomFloat', owner: C) -> V:
        return getattr(instance, self.name)

    def __set__(self, instance: 'CustomFloat', value: V) -> None:
        if not isinstance(value, float):
            raise ValueError('Must be float')

        if self.left is None and self.right is None:
            setattr(instance, self.name, value)
        elif self.left is None and self.right is not None:
            if value >= self.right:
                raise ValueError(f'Cannot be equal or bigger than {self.right}')
        elif self.right is None and self.left is not None:
            if value < self.left:
                raise ValueError(f'Cannot be smaller than {self.right}')
        else:
            if (self.right is not None and self.left is not None) and self.left <= value < self.right:
                setattr(instance, self.name, value)
            else:
                raise ValueError(f'Cannot be not in range [{self.left}:{self.right}]')
        setattr(instance, self.name, value)

    def __set_name__(self, owner: C, name: str) -> None:
        self.name = f'_{name.lower()}'
