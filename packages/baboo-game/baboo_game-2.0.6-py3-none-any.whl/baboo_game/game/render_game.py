import sys

from .config import color_config as color
from .config import text_constant as text
from .config import game_config as cfg
from .library.abstract_dice import Dice, D4, D6, D8
from .baboo_game import BabooGame


class RanderGame:
    def __init__(self):
        print("\x1b[8;43;98t")  # This line is for resizing user terminal
        print(self.__show_text(text.WELCOME_MESSAGE, color.YELLOW))
        print(self.__show_text(text.DICE_IMAGE, color.BLUE))
        self.__player_name = self.__get_player_name()
        self.__board = Dice(D4, D4)
        self.__game = BabooGame(self.__board, self.__player_name)
        self.__round = 1

    def __get_player_name(self):
        # name = input(self.__show_text("Please insert your name: "))
        name = "STRANGER"
        return name

    def __show_text(self, text, col=color.WHITE):
        return f"{col}{text}{color.RESET}"

    def __continue(self):
        self.__game.roll()

    def __roll_specific(self):
        while True:
            dice = self.__game.dice
            try:
                pos = input(self.__show_text(f"Select positions that you want to keep start from 1 to {len(dice)}: "))
                pos = list(map(lambda x: int(x) - 1, pos.split()))
                if max(pos) > (len(dice) - 1):
                    raise Exception
                else:
                    self.__game.roll(pos)
                    return
            except Exception:
                print(self.__show_text("Please insert a valid position ", color.RED))

    def __add_die(self, die):
        while True:
            position = input(
                self.__show_text("Enter position to replace your die or press enter to append to the end: "))
            try:
                if position == "":
                    print("empty")
                    self.__game.add_dice(die)
                    return
                else:
                    self.__game.dice[int(position) - 1] = die()
                    return
            except Exception:
                print(self.__show_text(f"Wrong position please please select between 1 and {len(self.__game.dice)}",
                                       color.RED))

    def __show_die_menu(self):
        print(self.__show_text(f"""
1. D4({cfg.DIE4_COST} Cr.)     2. D6({cfg.DIE6_COST} Cr.)      3. D8({cfg.DIE8_COST} Cr.)      4. Exit
        """))
        current_balance = self.__game.credit_balance
        while True:
            menu_number = input(self.__show_text("Select Die you want to buy: "))
            try:
                if 1 <= int(menu_number) <= 4:
                    match int(menu_number):
                        case 1:
                            if current_balance >= cfg.DIE4_COST + cfg.ROLL_COST:
                                self.__game.credit_balance -= cfg.DIE4_COST
                                self.__add_die(D4)
                                break
                        case 2:
                            if current_balance >= cfg.DIE6_COST + cfg.ROLL_COST:
                                self.__game.credit_balance -= cfg.DIE6_COST
                                self.__add_die(D6)
                                break
                        case 3:
                            if current_balance >= cfg.DIE8_COST + cfg.ROLL_COST:
                                self.__game.credit_balance -= cfg.DIE8_COST
                                self.__add_die(D8)
                                break
                        case 4:
                            break
                else:
                    raise Exception
            except Exception:
                print(self.__show_text("Select a valid menu number between 1 and 4: ", color.RED))

    def __withdraw(self):
        current_balance = self.__game.credit_balance
        print(self.__show_text(text.CONGRATULATIONS % current_balance, color.GREEN))
        # print(self.__show_text(WIN_AMOUNT % current_balance, color.GREEN))
        sys.exit()

    def __show_menu(self):

        print(self.__show_text("""
1. Continue      2. Roll specific dice      3. Add new die     4. Withdraw
        """))

        while True:
            menu_number = input(self.__show_text("Please chose a menu number: "))
            try:
                if 1 <= int(menu_number) <= 4:
                    match int(menu_number):
                        case 1:
                            self.__continue()
                        case 2:
                            self.__roll_specific()
                        case 3:
                            self.__show_die_menu()
                        case 4:
                            self.__withdraw()
                    break
                else:
                    raise Exception

            except Exception:
                print(self.__show_text("Please select a menu number between 1-4", color.RED))

    def __display_board(self):
        dice_list = self.__game.dice

        print(self.__show_text(f"\n{'▔' * 76}"))
        print(self.__show_text("Round:"), self.__show_text(self.__round, color.GREEN), end="    ")

        status_lose = self.__show_text("Lose", color.RED)
        status_win = self.__show_text("Win", color.GREEN)

        if self.__game.check_winner():
            print(self.__show_text("Status:"), status_win, end="     ")
        else:
            print(self.__show_text("Status:"), status_lose, end="     ")

        print(self.__show_text(f"Balance: {self.__game.credit_balance}"), end="     ")
        print(end="\n\n")

        for die in dice_list:
            print("    ", self.__show_text(die.face, color.Fore.LIGHTCYAN_EX), end="       ")
        print()

        for line in range(5):
            for die in dice_list:
                print(self.__show_text(text.DICE.get(die.face)[line], color.BLUE), end="  ")
            print()

        for die in dice_list:
            print("    ", self.__show_text(type(die).__name__, color.MAGENTA), end="      ")
        print(end="\n")

        print(self.__show_text(f"{'▁' * 76}"), end="\n\n")

    def play(self):
        input("Press ENTER to start the game: ")
        print(self.__show_text(text.START_GAME))
        self.__game.credit_balance -= cfg.ROLL_COST
        while self.__game.credit_balance >= cfg.ROLL_COST:
            if self.__game.check_winner():
                self.__game.credit_balance += self.__game.total_points
                self.__display_board()
                self.__game.roll()
                self.__show_menu()
                self.__round += 1
            else:
                self.__display_board()
                self.__show_menu()
                self.__round += 1
        print(self.__show_text(text.GAME_OVER, color.RED))
