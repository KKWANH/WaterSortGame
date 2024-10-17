from game.game import Game
from game.mod  import GameMod

if __name__ == "__main__":
    # Parameters: bottles, capacity, colors, game_mode
    game = Game(6, 4, 4, GameMod.NORMAL)
    game.start()