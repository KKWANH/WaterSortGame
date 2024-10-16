from game.game import Game

if __name__ == "__main__":
    # Parameters: bottles, capacity, colors, empty_cells, game_mode
    game = Game(6, 4, 4, 4, "NORMAL")
    game.start()