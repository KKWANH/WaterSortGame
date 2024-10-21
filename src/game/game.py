
import random
import csv
import copy

from util.util import print_error, print_debug, print_info
from game.state import GameState

class Game:
    def __init__(self, num_bottles, capacity, num_colors):
        # Check if input values are valid
        if num_bottles < 1:
            print_error("Number of bottles must be at least 1.")
            self.GAMESTATE = GameState.FAILURE
            return
        if capacity < 1:
            print_error("Capacity must be at least 1.")
            self.GAMESTATE = GameState.FAILURE
            return
        if num_colors < 1:
            print_error("Number of colors must be at least 1.")
            self.GAMESTATE = GameState.FAILURE
            return

        # Value setting
        self.GAMESTATE = GameState.WAITING
        self.num_bottles = num_bottles                               # Number of bottles
        self.capacity = capacity                                     # Cell capacity of each bottle
        self.num_colors = num_colors                                 # Number of colors
        self.total_cells = self.num_bottles * self.capacity          # Total number of cells
        self.colored_cells = self.num_colors * self.capacity         # Total colored cells
        self.empty_cells = self.total_cells - self.colored_cells     # Total empty cells

        self.moves_history = []    # To keep track of moves for export/import
        self.initial_puzzle = []   # To store the initial state of the puzzle
        self.is_game_solved = False  # To mark whether the game was solved

        self.colors = []           # Color pool
        self.puzzle = []           # Current puzzle state

        self.initialize()

    def initialize(self):
        # Check total number of cells consistency
        if self.total_cells <= 0:
            print_error("Total number of cells must be positive.")
            self.GAMESTATE = GameState.FAILURE
            return

        # Ensure there is at least one empty cell for movement
        if self.empty_cells // self.capacity < 1:
            print_error("There must be at least one empty bottle to allow for movement.")
            self.GAMESTATE = GameState.FAILURE
            return

        # Ensure bottle capacity compatibility
        if self.total_cells % self.capacity != 0:
            print_error("Total number of cells must be divisible by bottle capacity.")
            self.GAMESTATE = GameState.FAILURE
            return

        # Ensure number of bottles vs number of colors compatibility
        if self.num_bottles <= self.num_colors:
            print_error("Number of bottles must be greater than number of colors.")
            self.GAMESTATE = GameState.FAILURE
            return

        # Generate color distribution ensuring each color fits within the bottle capacity
        self.colors = self.generate_colors()

        # Generate the initial puzzle state
        self.puzzle = self.generate_puzzle_state()

        # Store the initial state of the puzzle
        self.initial_puzzle = copy.deepcopy(self.puzzle)

        self.GAMESTATE = GameState.SUCCESS

    def generate_colors(self):
        """
        Generate a pool of colors based on the number of colors and capacity.
        Shuffle the pool to randomize color distribution.
        """
        color_pool = []
        for color in range(1, self.num_colors + 1):
            color_pool.extend([color] * self.capacity)

        random.shuffle(color_pool)
        return color_pool

    def generate_puzzle_state(self):
        """
        Generate the initial puzzle state by distributing colors into bottles.
        """
        bottles = [[] for _ in range(self.num_bottles)]
        cell_index = 0

        for bottle in bottles:
            while len(bottle) < self.capacity and cell_index < len(self.colors):
                bottle.append(self.colors[cell_index])
                cell_index += 1

        return bottles

    def move(self, source, destination) -> bool:
        """
        Move all the same color from the top of 'source' to 'destination'.
        Return True if the move is successful, otherwise False.
        """
        # Check if source and destination bottle indexes are valid
        if not (0 <= source < self.num_bottles) or not (0 <= destination < self.num_bottles):
            return False  # Invalid bottle index

        source_bottle = self.puzzle[source]
        dest_bottle = self.puzzle[destination]

        # Cannot move from an empty source bottle
        if not source_bottle:
            return False

        # Top color of the source bottle
        top_color = source_bottle[-1]

        # Destination bottle must be either empty or have the same top color
        if dest_bottle and dest_bottle[-1] != top_color:
            return False

        # Count how many top-color cells can be moved
        move_count = 0
        while move_count < len(source_bottle) and source_bottle[-(move_count + 1)] == top_color:
            move_count += 1

        # Check available space in the destination bottle
        available_space = self.capacity - len(dest_bottle)

        if move_count > available_space:
            return False  # Not enough space in the destination bottle

        # Perform the move
        dest_bottle.extend(source_bottle[-move_count:])
        del source_bottle[-move_count:]

        # Record the move
        self.moves_history.append((source, destination))

        return True

    def is_solved(self):
        """
        Check if the game is solved: all bottles should either be empty or filled with one color.
        """
        for bottle in self.puzzle:
            if not bottle:
                continue  # Ignore empty bottles
            if len(bottle) != self.capacity or len(set(bottle)) != 1:
                return False  # Bottle must be full and contain only one color
        return True

    def export_game(self, filename):
        """
        Export the game data to a CSV file, including initial state, moves, and final status.
        """
        try:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                # Write initial puzzle state
                writer.writerow(['Initial Puzzle State'])
                for bottle in self.initial_puzzle:
                    writer.writerow(bottle)
                writer.writerow([])  # Empty line

                # Write moves history
                writer.writerow(['Moves History'])
                writer.writerow(['source', 'destination'])
                for move in self.moves_history:
                    writer.writerow([move[0], move[1]])
                writer.writerow([])  # Empty line

                # Write final status
                writer.writerow(['Game Solved', self.is_game_solved])
            print_info(f"Game exported successfully to {filename}.")
        except Exception as e:
            print_error(f"Failed to export game: {e}")

    def import_game(self, filename):
        """
        Import game data from a CSV file and replay the game.
        """
        try:
            with open(filename, 'r') as csvfile:
                reader = csv.reader(csvfile)
                content = list(reader)

                # Extract initial puzzle state
                initial_state_index = content.index(['Initial Puzzle State']) + 1
                moves_history_index = content.index(['Moves History'])
                initial_puzzle_data = content[initial_state_index:moves_history_index - 1]

                # Reconstruct the initial puzzle state
                self.initial_puzzle = [list(map(int, row)) for row in initial_puzzle_data]
                self.puzzle = copy.deepcopy(self.initial_puzzle)

                # Reset moves history
                self.moves_history = []

                # Extract moves history
                moves_data = content[moves_history_index + 2:]  # Skip 'Moves History' and headers
                for row in moves_data:
                    if not row:
                        continue
                    if row[0] == 'Game Solved':
                        # Read final status
                        self.is_game_solved = row[1] == 'True'
                        break
                    source = int(row[0])
                    destination = int(row[1])
                    if not self.move(source, destination):
                        print_error(f"Invalid move from {source + 1} to {destination + 1}.")
                        break

                print_info("Game replayed successfully.")
                return True
        except Exception as e:
            print_error(f"Failed to import game: {e}")
            return False
