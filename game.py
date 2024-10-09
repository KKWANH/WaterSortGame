# game.py
from util import print_error
import random
import copy

class GameMod:
    NORMAL = 0
    HIDDEN = 1

    VALID_MOD = {
        "NORMAL": NORMAL,
        "HIDDEN": HIDDEN,
        0: NORMAL,
        1: HIDDEN
    }

    @classmethod
    def isValid(cls, _mod):
        return _mod in cls.VALID_MOD

    @classmethod
    def get(cls, _mod):
        return cls.VALID_MOD.get(_mod)

class Game:
    def __init__(self, _bottles, _capacity, _colors, _empty, _mod):
        try:
            # Parameter value range check
            if _bottles < 1:
                raise ValueError(f"Argument [_bottles] is not valid. Number should be at least 1.")
            if _capacity < 1:
                raise ValueError(f"Argument [_capacity] is not valid. Number should be at least 1.")
            if _colors < 1:
                raise ValueError(f"Argument [_colors] is not valid. Number should be at least 1.")
            if _empty < 1:
                raise ValueError(f"Argument [_empty] is not valid. Number should be at least 1.")
            if not GameMod.isValid(_mod):
                raise ValueError(f"Argument [_mod] is not valid. Should be 0 (Normal) or 1 (Hidden).")

            # Value setting
            self.GAMEMOD = GameMod.get(_mod)
            self.N = _bottles            # Number of bottles
            self.C = _capacity           # Cell capacity of each bottle
            self.K = _colors             # Number of colors
            self.E = _empty              # Number of empty cells
            self.T = self.N * self.C - self.E  # Total number of colored cells

            # Rule 1: Total Number of Cells Consistency
            if self.T <= 0:
                raise ValueError("Total number of colored cells must be positive.")

            # Rule 2: Minimum Empty Cells for Movement
            if self.E < 1:
                raise ValueError("There must be at least one empty cell to allow for movement.")

            # Rule 3: Bottle Capacity Compatibility
            if self.T % self.C != 0:
                raise ValueError("The total number of colored cells must be divisible by the bottle capacity.")

            # Rule 4: Number of Bottles vs Number of Colors
            if self.N < self.K:
                raise ValueError("Number of bottles must be at least equal to the number of colors.")

            # Rule 5: Color Cell Counts Compatibility (Dynamic Color Distribution)
            # Allow variable counts of cells per color, ensuring they sum up to T

            # Generate random distribution of cells per color
            self.color_counts = self.generate_color_counts()

            # Rule 7: Constraints on Total Cells and Colors
            if sum(self.color_counts.values()) != self.T:
                raise ValueError("Sum of cells per color must equal the total number of colored cells.")

            # Rule 8: Allowance for Game Rules
            # Ensure that the initial state allows for legal moves according to the game rules
            # This will be handled during the puzzle generation

            # Generate the initial puzzle state
            self.initial_state = self.generate_puzzle_state()

            # Verify solvability of the puzzle
            if not self.is_solvable():
                raise ValueError("Generated puzzle is not solvable with the given parameters.")

        except Exception as e:
            print_error(f"Error initializing the game: {e}")

    def generate_color_counts(self):
        """
        Generate a random distribution of cells per color,
        ensuring that the total cells equal T and that each color
        can fit into bottles without exceeding capacity.
        """
        remaining_cells = self.T
        color_counts = {}
        colors = list(range(1, self.K + 1))

        # Ensure each color has at least one cell
        for color in colors:
            min_cells = 1
            max_cells = min(self.C * self.N - (self.K - len(color_counts) - 1), remaining_cells - (self.K - len(color_counts) - 1))
            count = random.randint(min_cells, max_cells)
            color_counts[color] = count
            remaining_cells -= count

        # Distribute remaining cells
        while remaining_cells > 0:
            color = random.choice(colors)
            if color_counts[color] < self.N * self.C:
                color_counts[color] += 1
                remaining_cells -= 1

        return color_counts

    def generate_puzzle_state(self):
        """
        Generate the initial puzzle state based on the color counts.
        """
        # Create a list of all colored cells
        cells = []
        for color, count in self.color_counts.items():
            cells.extend([color] * count)

        # Shuffle the cells to create a random starting state
        random.shuffle(cells)

        # Create empty bottles
        bottles = [[] for _ in range(self.N)]

        # Fill the bottles with cells
        cell_index = 0
        for bottle in bottles:
            while len(bottle) < self.C and cell_index < len(cells):
                bottle.append(cells[cell_index])
                cell_index += 1

        # Ensure that empty cells are accounted for
        # Remove cells to create empty spaces (if E > 0)
        if self.E > 0:
            total_cells_to_remove = self.E
            for bottle in bottles:
                while bottle and total_cells_to_remove > 0:
                    bottle.pop()
                    total_cells_to_remove -= 1
                if total_cells_to_remove == 0:
                    break

        return bottles

    def is_solvable(self):
        """
        Determine if the generated puzzle is solvable.
        """
        # For the purposes of this example, we'll assume the puzzle is solvable.
        # Implement a solving algorithm to verify solvability.
        # This can be complex and may involve BFS, DFS, or other search algorithms.
        # For now, we return True as a placeholder.
        return True

    def solve_puzzle(self):
        """
        Solve the puzzle using an appropriate algorithm.
        """
        # Implement the solving logic here.
        pass

    def print_puzzle(self):
        """
        Print the puzzle state for debugging purposes.
        """
        for idx, bottle in enumerate(self.initial_state):
            print(f"Bottle {idx + 1}: {bottle}")
