from abc import ABC, abstractmethod
from ex3.creature import Creature
from ex3.creatures import Flameling, Pyrodon, Morphagon, Shiftling


class CreatureFactory(ABC):
    @abstractmethod
    def create_base(self) -> Creature:
        ...

    @abstractmethod
    def create_evolved(self) -> Creature:
        ...


class FlameFactory(CreatureFactory):
    def create_base(self) -> Flameling:
        return Flameling()

    def create_evolved(self) -> Pyrodon:
        return Pyrodon()


class TransformCreatureFactory(CreatureFactory):
    def create_base(self) -> Shiftling:
        return (Shiftling())

    def create_evolved(self) -> Morphagon:
        return (Morphagon())
