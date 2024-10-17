import random

from util.util import print_error, print_debug, print_info
from game.mod import GameMod
from game.state import GameState

class Game:
    def __init__(self, _bottles, _capacity, _colors, _mod):
        # Check if input values are valid
        if _bottles < 1:
            print_error("Number of bottles [_bottles] must be at least 1.")
            return
        if _capacity < 1:
            print_error("Capacity [_capacity] must be at least 1.")
            return
        if _colors < 1:
            print_error("Number of colors [_colors] must be at least 1.")
            return
        if _mod not in GameMod:
            print_error("Game mode [_mod] is invalid. Should be 0 (Normal) or 1 (Hidden).")
            return

        # Value setting
        self.GAMEMOD = _mod
        self.GAMESTATE = GameState.WAITING
        self.num_bottles = _bottles                                 # Number of bottles
        self.capacity = _capacity                                   # Cell capacity of each bottle
        self.num_colors = _colors                                   # Number of colors
        self.total_cells = self.num_bottles * self.capacity         # Total number of cells
        self.colored_cells = self.num_colors * self.capacity        # Total colored cells
        self.empty_cells = self.total_cells - self.colored_cells    # Total empty cells

    def initialize(self):
        # Check total number of cells consistency
        if self.total_cells <= 0:
            print_error("Total number of cells must be positive.")
            return

        # Ensure there is at least one empty cell for movement
        if self.empty_cells // self.capacity < 1:
            print_error("There must be at least one empty cell to allow for movement.")
            return

        # Ensure bottle capacity compatibility
        if self.total_cells % self.capacity != 0:
            print_error("Total number of cells must be divisible by bottle capacity.")
            return

        # Ensure number of bottles vs number of colors compatibility
        if self.num_bottles <= self.num_colors:
            print_error("Number of bottles must be greater than number of colors.")
            return

        # Generate color distribution ensuring each color fits within the bottle capacity
        self.capacityolors = self.generate_colors()

        # Generate the initial puzzle state
        self.puzzle = self.generate_puzzle_state()

        self.GAMESTATE = GameState.SUCCESS
    
    def generate_colors(self):
        """
        Generate a pool of colors based on the number of colors (K) and capacity (C).
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
            while len(bottle) < self.capacity and cell_index < len(self.capacityolors):
                bottle.append(self.capacityolors[cell_index])
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

    def print_puzzle(self):
        max_height = max(len(bottle) for bottle in self.puzzle)
        for level in range(max_height, 0, -1):
            line = ''
            for bottle in self.puzzle:
                if len(bottle) >= level:
                    line += f'| {bottle[level - 1]} | '
                else:
                    line += '|   | '
            print(line)
        print('-' * (self.num_bottles * 6))

    def get_valid_int_input(self, prompt):
        while True:
            user_input = input(prompt)
            if user_input.isdigit():
                return int(user_input) - 1
            else:
                print_error("Invalid input. Please enter a number.")

    def start(self):
        try:
            print_info("Initializing.")
            self.initialize()
            if self.GAMESTATE == GameState.FAILURE:
                return self.GAMESTATE

            print_info("Game Start.")
            while True:
                self.print_puzzle()
                from_bottle = self.get_valid_int_input("From which bottle? ")
                to_bottle = self.get_valid_int_input("To which bottle? ")

                if self.move(from_bottle, to_bottle):
                    print_info("Move successful.")
                    if self.is_solved():
                        print_info("Congratulations! You've solved the puzzle!")
                        self.print_puzzle()
                        return True
                else:
                    print_info("Invalid move. Try again.")
            
        except Exception as e:
            print_error(f"Error starting game: {e}")
