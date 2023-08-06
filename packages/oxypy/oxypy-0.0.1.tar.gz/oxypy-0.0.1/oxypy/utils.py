from typing import Generic, Protocol, Type, TypeVar

T_co = TypeVar("T_co", covariant=True)


class Null:
    def __repr__(self) -> str:
        return "<NULL>"


class Panic(Exception):
    ...  # noqa


class Default(Generic[T_co], Protocol):
    @classmethod
    def default(cls: Type[T_co]) -> T_co:
        ...  # noqa


NULL = Null()
