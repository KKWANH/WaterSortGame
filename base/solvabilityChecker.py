class SolvabilityChecker:
    @staticmethod
    def is_solvable(game_state):
        # Mathematical logic to check solvability
        color_counts = {}
        for bottle in game_state.bottles:
            for color_id in bottle.contents:
                color_counts[color_id] = color_counts.get(color_id, 0) + 1

        # Verify that each color can fill a bottle
        for count in color_counts.values():
            if count != bottle.capacity:
                return False
        
        # Check are there enough empty spaces
        total_space = sum(bottle.capacity - len(bottle.contents) for bottle in game_state.bottles)
        if total_space < bottle.capacity:
            return False

        # Additional mathematical & logical checks...
        
        return True
