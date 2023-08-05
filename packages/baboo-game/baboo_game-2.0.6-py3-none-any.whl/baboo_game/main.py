if __package__ is None or __package__ == '':
    # uses current directory visibility
    from game.render_game import RanderGame
else:
    # uses current package visibility
    from .game.render_game import RanderGame


def start():
    game = RanderGame()
    game.play()


if __name__ == "__main__":
    start()
