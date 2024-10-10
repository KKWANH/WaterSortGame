# game.py
from util import print_error
import random
from collections import deque

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
            # Generate random distribution of cells per color
            self.color_counts = self.generate_color_counts()

            # Rule 7: Constraints on Total Cells and Colors
            if sum(self.color_counts.values()) != self.T:
                raise ValueError("Sum of cells per color must equal the total number of colored cells.")

            # Rule 8: Allowance for Game Rules
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

        # Initially assign zero cells to each color
        for color in colors:
            color_counts[color] = 0

        # Distribute the remaining cells
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
        total_cells_to_remove = self.E
        while total_cells_to_remove > 0:
            for bottle in bottles:
                if bottle and total_cells_to_remove > 0:
                    bottle.pop()
                    total_cells_to_remove -= 1
                if total_cells_to_remove == 0:
                    break

        return bottles

    def is_solvable(self):
        """
        Determine if the generated puzzle is solvable using BFS.
        """
        from collections import deque

        # Define the goal state check function
        def is_goal_state(state):
            for bottle in state:
                if not bottle:
                    continue
                if len(bottle) > self.C:
                    return False
                if len(set(bottle)) != 1:
                    return False
            return True

        # Serialize the state for hashing
        def serialize_state(state):
            return tuple(tuple(bottle) for bottle in state)

        # Initialize BFS
        initial_state = [list(bottle) for bottle in self.initial_state]
        visited = set()
        queue = deque()

        serialized_initial = serialize_state(initial_state)
        queue.append(initial_state)
        visited.add(serialized_initial)

        max_steps = 100000  # Limit to prevent infinite loops

        steps = 0
        while queue and steps < max_steps:
            current_state = queue.popleft()
            steps += 1

            # Check if the current state is the goal state
            if is_goal_state(current_state):
                return True

            # Generate all valid moves from the current state
            for i in range(self.N):
                for j in range(self.N):
                    if i == j:
                        continue
                    source = current_state[i]
                    dest = current_state[j]

                    if not source:
                        continue  # Can't pour from empty bottle
                    if len(dest) >= self.C:
                        continue  # Can't pour into a full bottle

                    # Get the top color to pour
                    color_to_pour = source[-1]

                    # Check if we can pour
                    if not dest or dest[-1] == color_to_pour:
                        # Find how many cells we can pour
                        pour_count = 1
                        while (len(source) - pour_count >= 0 and
                               source[-pour_count] == color_to_pour and
                               len(dest) + pour_count <= self.C):
                            pour_count += 1
                        pour_count -= 1  # Adjust since we over-counted

                        # Perform the pour
                        new_state = [list(b) for b in current_state]
                        moving_cells = [new_state[i].pop() for _ in range(pour_count)]
                        new_state[j].extend(reversed(moving_cells))

                        # Serialize the new state
                        serialized_new_state = serialize_state(new_state)

                        if serialized_new_state not in visited:
                            visited.add(serialized_new_state)
                            queue.append(new_state)

        # If we exit the loop without returning True, the puzzle is not solvable
        return False

    def print_puzzle(self):
        """
        Print the puzzle state for debugging purposes.
        """
        for idx, bottle in enumerate(self.initial_state):
            print(f"Bottle {idx + 1}: {bottle}")
