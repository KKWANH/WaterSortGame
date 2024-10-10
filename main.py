from game import Game, GameMod

if __name__ == "__main__":
    # Parameters: bottles, capacity, colors, empty_cells, game_mode
    game = Game(6, 4, 4, 4, GameMod.NORMAL)
    if game.is_solvable():
        game.print_puzzle()
    else:
        print("Generated puzzle is not solvable.")