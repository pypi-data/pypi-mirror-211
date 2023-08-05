from .library.abstract_dice import *
from .config.game_config import *


class BabooGame(DiceGameBase):
    def __init__(self, dice_board: "Dice", player_name: str):
        super().__init__(dice_board, player_name)
        self._credit_balance = INITIAL_BALANCE

    @property
    def dice(self):
        return self._dice_board.dice

    @property
    def player_name(self):
        return self._player_name

    @property
    def total_points(self) -> int:
        return self._dice_board.plus(len(self._dice_board.dice)).total * ROLL_COST

    @property
    def credit_balance(self):
        return self._credit_balance

    @credit_balance.setter
    def credit_balance(self, amount):
        self._credit_balance = amount

    def check_winner(self) -> bool:
        return len(set(die.face for die in self._dice_board.dice)) == 1

    def roll(self, roll_pos: Iterable[int] = None) -> None:
        if self._credit_balance >= ROLL_COST:
            if roll_pos:
                self._dice_board.to_be_rolled(roll_pos).roll()
            else:
                self._dice_board.roll()

            self._credit_balance -= ROLL_COST
        else:
            raise PermissionError("Not enough balance")

    def add_dice(self, die: Type["DieBase"]):
        self._dice_board += die

    def replace_die(self, pos, die):
        self._dice_board[pos] = die()
