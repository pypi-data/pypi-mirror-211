from abc import ABC, abstractmethod
from random import randint
from typing import Set, Iterable, Type


class DiceGameBase(ABC):
    def __init__(self, dice_board: "Dice", player_name: str):
        self._dice_board = dice_board
        self._player_name = player_name

    @abstractmethod
    def check_winner(self) -> bool:
        ...

    @abstractmethod
    def roll(self) -> None:
        ...

    @abstractmethod
    def add_dice(self, die: Type["DieBase"]) -> None:
        ...

    @property
    @abstractmethod
    def total_points(self) -> int:
        ...


class DieBase(ABC):
    def __init__(self) -> None:
        self.face = None
        self.roll()

    @abstractmethod
    def roll(self) -> None:
        ...

    def __repr__(self) -> str:
        return str(self.face)


class D4(DieBase):
    def roll(self) -> None:
        self.face = randint(1, 4)


class D6(DieBase):
    def roll(self) -> None:
        self.face = randint(1, 6)


class D8(DieBase):
    def roll(self) -> None:
        self.face = randint(1, 8)


class Dice:

    def __init__(self, *die_classes) -> None:
        self.__dice = [dc() for dc in die_classes]
        self.__adjust: int = 0
        self.rolled_pos: Set[int] = set()

    @property
    def total(self) -> int:
        return sum(d.face for d in self.__dice) + self.__adjust

    @property
    def dice(self):
        return self.__dice

    @dice.setter
    def dice(self, value):
        raise NotImplementedError

    def plus(self, adjust: int = 0):
        self.__adjust = adjust
        return self

    def roll(self) -> None:
        if not self.rolled_pos:
            for die in self.dice:
                die.roll()
        else:
            for i in self.rolled_pos:
                self.__dice[i].roll()
        self.rolled_pos = set()

    def to_be_rolled(self, pos: Iterable[int]):
        if not all(0 <= n < len(self.__dice) for n in pos):
            raise IndexError("Some indices are out of range")
        self.rolled_pos = set(pos)
        return self

    def __repr__(self):
        return str(self.__dice)

    def __add__(self, other):
        if issubclass(other, DieBase):
            new_classes = [type(d) for d in self.__dice] + [other]  # D4, D6, D8
            new = Dice(*new_classes)
            return new
        raise ValueError(f"Type {type(other)} not supported")

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        if issubclass(other, DieBase):
            self.__dice.append(other())
            return self

    def __mul__(self, other):
        if isinstance(other, int):
            new_classes = [type(d) for d in self.__dice] * other
            new = Dice(*new_classes)
            return new
        raise NotImplementedError(f"Value of type {type(other)} is not supported")

    def __imul__(self, other):
        if isinstance(other, int):
            new_dice = [type(d) for d in self.__dice] * other
            self.__dice = [die() for die in new_dice]
            return self
        raise NotImplementedError(f"Value of type {type(other)} is not supported")

    def __rmul__(self, other):
        raise NotImplementedError
