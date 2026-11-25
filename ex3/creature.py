from abc import ABC, abstractmethod


class Creature(ABC):
    def __init__(self, name: str, ctype: str) -> None:
        self.name: str = name
        self.ctype: str = ctype

    @abstractmethod
    def attack(self) -> str:
        ...

    def describe(self) -> str:
        return (f"{self.name} is a {self.ctype} creature")


class TransformCapability(ABC):
    def __init__(self) -> None:
        self._transformed: bool = False

    @abstractmethod
    def transform(self) -> str:
        ...

    @abstractmethod
    def revert(self) -> str:
        ...
