from game.game  import Game
from game.state import GameState
from game.gui   import GameGUI
from util.util  import print_error

if __name__ == "__main__":
    num_bottles = 6
    capacity = 4
    num_colors = 4

    game = Game(num_bottles, capacity, num_colors)
    if game.GAMESTATE == GameState.SUCCESS:
        gui = GameGUI(game)
        gui.start()
    else:
        print_error("Failed to initialize the game.")