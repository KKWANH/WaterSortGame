from base.bottle import Bottle
from base.gameState import GameState
from base.solvabilityChecker import SolvabilityChecker

class LevelGenerator:
    def __init__(self, level):
        if not level.isnumeric():
            assert TypeError("level must be number")
        self.level = level
        self.capacity = 4  # Fixed
        self.num_colors = None
        self.num_bottles = None
        self.generate_parameters()

    def generate_parameters(self):
        # 레벨에 따른 num_colors와 num_bottles 결정
        self.num_colors = min(2 + self.level // 5, 12)  # 최대 12색
        extra_bottles = max(2 - self.level // 10, 1)    # 빈 병의 수를 레벨에 따라 조절
        self.num_bottles = self.num_colors + extra_bottles

    def generate_level(self):
        # 해결 가능한 GameState 생성
        initial_state = self.create_initial_state()
        if SolvabilityChecker.is_solvable(initial_state):
            return initial_state
        else:
            self.generate_parameters()
            return self.generate_level()

    def create_initial_state(self):
        import random
        total_units_per_color = self.capacity  # 각 색상은 병 하나를 채움
        colors = []
        for color_id in range(1, self.num_colors + 1):
            colors.extend([color_id] * total_units_per_color)

        random.shuffle(colors)

        bottles = []
        color_index = 0
        num_filled_bottles = self.num_bottles - (self.num_bottles - self.num_colors)
        for _ in range(num_filled_bottles):
            bottle = Bottle(self.capacity)
            bottle.contents = colors[color_index:color_index + self.capacity]
            color_index += self.capacity
            bottles.append(bottle)

        # 빈 병 추가
        for _ in range(self.num_bottles - num_filled_bottles):
            bottles.append(Bottle(self.capacity))

        # 병 순서 섞기
        random.shuffle(bottles)

        return GameState(bottles)
