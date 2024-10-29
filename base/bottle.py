class Bottle:
    def __init__(self, capacity):
        self.capacity = capacity
        self.contents = []  # List of color IDs (integers)

    def is_full(self):
        return len(self.contents) >= self.capacity

    def is_empty(self):
        return len(self.contents) == 0

    def top_color(self):
        return self.contents[-1] if not self.is_empty() else None

    def can_receive(self, color_id, amount):
        if self.is_full():
            return False
        if self.is_empty():
            return (len(self.contents) + amount) <= self.capacity
        return (self.top_color() == color_id) and ((len(self.contents) + amount) <= self.capacity)

    def pour_into(self, target_bottle):
        # TODO: Logic to pour contents into target bottle
        pass
