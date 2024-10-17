# game_gui.py

import pygame
import random
import sys

from util.util import print_error, print_debug, print_info
from game.game import Game


class GameGUI:
    def __init__(self, game: Game):
        self.game = game

        # Pygame initialization
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Water Sort Puzzle')
        self.clock = pygame.time.Clock()
        self.running = True

        # Colors
        self.assign_random_colors()  # Assign colors once at game start
        self.selected_bottle = None  # To track the selected bottle

        # Fonts
        self.font_small = pygame.font.SysFont('Arial', 24)
        self.font_large = pygame.font.SysFont('Arial', 48)

    def assign_random_colors(self):
        """
        Assign a random RGB color to each color number.
        """
        self.color_map = {}
        hues = [int(i * 360 / self.game.num_colors) for i in range(self.game.num_colors)]
        random.shuffle(hues)
        for i, color_num in enumerate(range(1, self.game.num_colors + 1)):
            hue = hues[i]
            color = pygame.Color(0)
            color.hsva = (hue, 100, 100, 100)
            self.color_map[color_num] = color

    def draw_puzzle(self):
        """
        현재 퍼즐 상태를 Pygame으로 그립니다.
        """
        self.screen.fill((30, 30, 30))  # 더 어두운 배경

        bottle_width = 60
        bottle_height = self.game.capacity * 30 + 20
        spacing = 20
        start_x = (self.screen_width - (self.game.num_bottles * (bottle_width + spacing))) // 2
        start_y = (self.screen_height - bottle_height) // 2 + 50  # 헤더 공간 확보

        for index, bottle in enumerate(self.game.puzzle):
            x = start_x + index * (bottle_width + spacing)
            y = start_y

            # 병 윤곽 그리기
            pygame.draw.rect(self.screen, (200, 200, 200), (x, y, bottle_width, bottle_height), 2)
            pygame.draw.rect(self.screen, (50, 50, 50), (x, y, bottle_width, bottle_height))

            # 선택된 병 강조 표시
            if self.selected_bottle == index:
                pygame.draw.rect(self.screen, (255, 215, 0), (x - 4, y - 4, bottle_width + 8, bottle_height + 8), 3)

            # 액체를 아래에서 위로 그리기
            liquid_height = (bottle_height - 20) / self.game.capacity
            num_liquids = len(bottle)
            for i in range(num_liquids):
                color_num = bottle[i]  # 병의 첫 번째 요소부터 접근 (맨 아래 요소)
                color = self.color_map.get(color_num, (255, 255, 255))
                rect = pygame.Rect(
                    x + 2,
                    y + bottle_height - 10 - (i + 1) * liquid_height,
                    bottle_width - 4,
                    liquid_height
                )
                pygame.draw.rect(self.screen, color, rect)

                # 층 사이 경계선 그리기
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

        # 헤더 그리기
        header_text = self.font_large.render("Water Sort Puzzle", True, (255, 255, 255))
        header_rect = header_text.get_rect(center=(self.screen_width // 2, 40))
        self.screen.blit(header_text, header_rect)

        pygame.display.flip()




    def get_bottle_at_pos(self, pos):
        """
        Determine which bottle was clicked based on the mouse position.
        """
        bottle_width = 60
        bottle_height = self.game.capacity * 30 + 20
        spacing = 20
        start_x = (self.screen_width - (self.game.num_bottles * (bottle_width + spacing))) // 2
        start_y = (self.screen_height - bottle_height) // 2 + 50  # Consider header space

        x, y = pos
        for index in range(self.game.num_bottles):
            bottle_x = start_x + index * (bottle_width + spacing)
            bottle_rect = pygame.Rect(bottle_x, start_y, bottle_width, bottle_height)
            if bottle_rect.collidepoint(x, y):
                return index
        return None

    def start(self):
        while self.running:
            self.clock.tick(60)  # Limit to 60 FPS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.handle_quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            self.draw_puzzle()

            if self.game.is_solved():
                self.game.is_game_solved = True
                self.display_win_message()
                pygame.time.delay(2000)
                self.handle_quit()

    def handle_click(self, pos):
        bottle_index = self.get_bottle_at_pos(pos)
        if bottle_index is not None:
            if self.selected_bottle is None:
                self.selected_bottle = bottle_index
            else:
                if self.selected_bottle != bottle_index:
                    if self.game.move(self.selected_bottle, bottle_index):
                        print_info(f"Moved from bottle {self.selected_bottle + 1} to {bottle_index + 1}")
                    else:
                        print_info("Invalid move.")
                self.selected_bottle = None

    def display_win_message(self):
        font = pygame.font.SysFont('Arial', 72)
        text = font.render("You Win!", True, (255, 215, 0))
        rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(text, rect)
        pygame.display.flip()

    def handle_quit(self):
        # Use GUI to ask if the player wants to export the game
        export = self.show_export_dialog()
        if export:
            filename = self.show_filename_input()
            if filename:
                self.game.export_game(filename)
        self.running = False
        pygame.quit()
        sys.exit()

    def show_export_dialog(self):
        """
        Display a GUI dialog asking if the player wants to export the game.
        Returns True if the player chooses to export, False otherwise.
        """
        dialog_width = 400
        dialog_height = 200
        dialog_rect = pygame.Rect(
            (self.screen_width - dialog_width) // 2,
            (self.screen_height - dialog_height) // 2,
            dialog_width,
            dialog_height
        )

        yes_button = pygame.Rect(dialog_rect.left + 50, dialog_rect.bottom - 80, 120, 50)
        no_button = pygame.Rect(dialog_rect.right - 170, dialog_rect.bottom - 80, 120, 50)

        running_dialog = True
        while running_dialog:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running_dialog = False
                    self.running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if yes_button.collidepoint(event.pos):
                        return True
                    elif no_button.collidepoint(event.pos):
                        return False

            # Draw dialog background with rounded corners
            self.draw_rounded_rect(self.screen, (50, 50, 50), dialog_rect, 10)
            pygame.draw.rect(self.screen, (255, 255, 255), dialog_rect, 2, border_radius=10)

            # Render text
            font = pygame.font.SysFont('Arial', 28)
            text_surface = font.render("Do you want to export your game?", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.screen_width // 2, dialog_rect.top + 60))
            self.screen.blit(text_surface, text_rect)

            # Draw buttons with rounded corners
            self.draw_rounded_rect(self.screen, (70, 130, 180), yes_button, 5)
            pygame.draw.rect(self.screen, (255, 255, 255), yes_button, 2, border_radius=5)
            yes_text = font.render("Yes", True, (255, 255, 255))
            yes_text_rect = yes_text.get_rect(center=yes_button.center)
            self.screen.blit(yes_text, yes_text_rect)

            self.draw_rounded_rect(self.screen, (200, 70, 70), no_button, 5)
            pygame.draw.rect(self.screen, (255, 255, 255), no_button, 2, border_radius=5)
            no_text = font.render("No", True, (255, 255, 255))
            no_text_rect = no_text.get_rect(center=no_button.center)
            self.screen.blit(no_text, no_text_rect)

            pygame.display.flip()

        return False

    def show_filename_input(self):
        """
        Display a GUI input box for the player to enter the filename.
        Returns the filename as a string.
        """
        dialog_width = 500
        dialog_height = 200
        dialog_rect = pygame.Rect(
            (self.screen_width - dialog_width) // 2,
            (self.screen_height - dialog_height) // 2,
            dialog_width,
            dialog_height
        )

        input_box = pygame.Rect(dialog_rect.left + 20, dialog_rect.centery - 20, dialog_width - 40, 40)
        input_text = ''
        active = True

        submit_button = pygame.Rect(dialog_rect.centerx - 60, dialog_rect.bottom - 60, 120, 50)

        running_dialog = True
        while running_dialog:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running_dialog = False
                    self.running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = True
                    else:
                        active = False

                    if submit_button.collidepoint(event.pos):
                        if input_text.strip() != '':
                            return input_text.strip()
                elif event.type == pygame.KEYDOWN and active:
                    if event.key == pygame.K_RETURN:
                        if input_text.strip() != '':
                            return input_text.strip()
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

            # Draw dialog background with rounded corners
            self.draw_rounded_rect(self.screen, (50, 50, 50), dialog_rect, 10)
            pygame.draw.rect(self.screen, (255, 255, 255), dialog_rect, 2, border_radius=10)

            # Render prompt text
            font = pygame.font.SysFont('Arial', 24)
            prompt_surface = font.render("Enter filename to export (e.g., game.csv):", True, (255, 255, 255))
            prompt_rect = prompt_surface.get_rect(midtop=(self.screen_width // 2, dialog_rect.top + 20))
            self.screen.blit(prompt_surface, prompt_rect)

            # Draw input box with rounded corners
            self.draw_rounded_rect(self.screen, (255, 255, 255), input_box, 5)
            pygame.draw.rect(self.screen, (0, 0, 0), input_box, 2, border_radius=5)
            input_surface = font.render(input_text, True, (0, 0, 0))
            self.screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))

            # Draw submit button
            self.draw_rounded_rect(self.screen, (70, 130, 180), submit_button, 5)
            pygame.draw.rect(self.screen, (255, 255, 255), submit_button, 2, border_radius=5)
            submit_text = font.render("Submit", True, (255, 255, 255))
            submit_text_rect = submit_text.get_rect(center=submit_button.center)
            self.screen.blit(submit_text, submit_text_rect)

            pygame.display.flip()

        return None

    def draw_rounded_rect(self, surface, color, rect, radius):
        """
        Draw a rectangle with rounded corners.
        """
        pygame.draw.rect(surface, color, rect, border_radius=radius)

