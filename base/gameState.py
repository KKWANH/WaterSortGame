import copy

class GameState:
    def __init__(self, _bottles, _history=None):
        self.bottles = _bottles
        self.history = _history or []

    def generate_valid_moves(self):
        pass

    def is_goal_state(self):
        pass

    def apply_move(self, _move):
        new_bottles = copy.deepcopy(self.bottles)
        source_bottle = new_bottles[_move.source]
        destination_bottle = new_bottles[_move.destination]

        color_to_move = source_bottle.top_color()
        amount_to_move = _move.amount

        source_bottle.contents = source_bottle.contents[:-amount_to_move]
        destination_bottle.contents.extend([color_to_move] * amount_to_move)

        new_history = self.history + [_move]
        return GameState(new_bottles, new_history)

    def encode_state(self):
        return tuple(tuple(bottle.contents) for bottle in self.bottles)
