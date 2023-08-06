from typing import TypeVar, Generic

from py_desc.base import Base

T = TypeVar('T', bound=dict)
C = TypeVar('C')

KT = TypeVar('KT')
VT = TypeVar('VT')


class SimpleDict(Base, Generic[KT, VT]):

    def __get__(self, instance: 'SimpleDict', owner: C) -> T:
        return getattr(instance, self.name)

    def __set__(self, instance: 'SimpleDict', value: T) -> None:
        if not isinstance(value, dict):
            raise ValueError('Must be dict')
        setattr(instance, self.name, value)

    def __set_name__(self, owner: C, name: str) -> None:
        self.name = f'_{name.lower()}'


# class Mapping(Base, Generic[KT, VT]):
#     def __get__(self, instance, owner):
#         return getattr(instance, self.name)
#
#     def __set__(self, instance, value):
#         if not isinstance(value, dict):
#             raise ValueError('Must be dict')
#         setattr(instance, self.name, value)
#
#     def __set_name__(self, owner, name):
#         self.name = f'_{name.lower()}'
#
#     def __getitem__(self, item: KT) -> VT:
#
#         return self.d[item]
#
#     def __len__(self) -> int:
#         return len(self.d)
#
#     def __iter__(self) -> Iterator[KT]:
#         return iter(self.d)
