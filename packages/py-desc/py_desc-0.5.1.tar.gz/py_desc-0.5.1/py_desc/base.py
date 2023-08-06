from abc import ABC, abstractmethod


class Base(ABC):
    @abstractmethod
    def __get__(self, instance, owner):  # type: ignore
        pass

    @abstractmethod
    def __set__(self, instance, value):  # type: ignore
        pass

    @abstractmethod
    def __set_name__(self, owner, name):  # type: ignore
        pass
