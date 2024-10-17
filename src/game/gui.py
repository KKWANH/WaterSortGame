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
        pygame.display.set_caption('Water Sort Puzzle')
        self.clock = pygame.time.Clock()
        self.running = True

        # Screen size
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)

        # Colors
        self.assign_random_colors()  # Assign colors once at game start
        self.selected_bottle = None  # To track the selected bottle

        # Fonts
        self.font_small = pygame.font.SysFont('Helvetica', 16)  # macOS style font
        self.font_large = pygame.font.SysFont('Helvetica', 32)

        # Color theme
        self.background_color = (30, 30, 30)  # Dark background
        self.bottle_outline_color = (200, 200, 200)
        self.bottle_fill_color = (50, 50, 50)
        self.selected_bottle_color = (255, 215, 0)  # Gold highlight

    def assign_random_colors(self):
        """
        Assign a unique RGB color to each color number.
        """
        self.color_map = {}
        hues = [int(i * 360 / self.game.num_colors) for i in range(self.game.num_colors)]
        random.shuffle(hues)
        for i, color_num in enumerate(range(1, self.game.num_colors + 1)):
            hue = hues[i]
            color = pygame.Color(0)
            color.hsva = (hue, 80, 90, 100)
            self.color_map[color_num] = color

    def draw_puzzle(self):
        """
        Draw the current puzzle state using Pygame.
        """
        self.screen.fill(self.background_color)  # Dark background

        # Responsive bottle size
        bottle_spacing = 20
        max_bottle_width = 80
        max_bottle_height = 300
        num_bottles = self.game.num_bottles
        capacity = self.game.capacity

        # Calculate bottle size
        bottle_width = min(max_bottle_width, (self.screen_width - (num_bottles + 1) * bottle_spacing) / num_bottles)
        bottle_height = min(max_bottle_height, (self.screen_height - 200))  # Reserve space for header and footer
        liquid_height = (bottle_height - 20) / capacity

        start_x = (self.screen_width - (num_bottles * (bottle_width + bottle_spacing) - bottle_spacing)) / 2
        start_y = (self.screen_height - bottle_height) / 2 + 30  # Adjust for header

        for index, bottle in enumerate(self.game.puzzle):
            x = start_x + index * (bottle_width + bottle_spacing)
            y = start_y

            # Draw bottle outline
            pygame.draw.rect(self.screen, self.bottle_fill_color, (x, y, bottle_width, bottle_height), border_radius=10)
            pygame.draw.rect(self.screen, self.bottle_outline_color, (x, y, bottle_width, bottle_height), 2, border_radius=10)

            # Highlight selected bottle
            if self.selected_bottle == index:
                pygame.draw.rect(self.screen, self.selected_bottle_color, (x - 3, y - 3, bottle_width + 6, bottle_height + 6), 3, border_radius=13)

            # Draw liquids from bottom to top
            num_liquids = len(bottle)
            for i in range(num_liquids):
                color_num = bottle[i]  # Access from first element
                color = self.color_map.get(color_num, (255, 255, 255))
                rect = pygame.Rect(
                    x + 5,
                    y + bottle_height - 10 - (i + 1) * liquid_height,
                    bottle_width - 10,
                    liquid_height
                )
                pygame.draw.rect(self.screen, color, rect, border_radius=3)

        # Draw header
        header_text = self.font_large.render("Water Sort Puzzle", True, (255, 255, 255))
        header_rect = header_text.get_rect(center=(self.screen_width // 2, 20))
        self.screen.blit(header_text, header_rect)

        pygame.display.flip()

    def get_bottle_at_pos(self, pos):
        """
        Determine which bottle was clicked based on the mouse position.
        """
        bottle_spacing = 20
        num_bottles = self.game.num_bottles
        capacity = self.game.capacity

        # Calculate bottle size
        bottle_width = min(80, (self.screen_width - (num_bottles + 1) * bottle_spacing) / num_bottles)
        bottle_height = min(300, (self.screen_height - 200))
        start_x = (self.screen_width - (num_bottles * (bottle_width + bottle_spacing) - bottle_spacing)) / 2
        start_y = (self.screen_height - bottle_height) / 2 + 30

        x, y = pos
        for index in range(num_bottles):
            bottle_x = start_x + index * (bottle_width + bottle_spacing)
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
                elif event.type == pygame.VIDEORESIZE:
                    self.screen_width, self.screen_height = event.size
                    self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
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
                        print_info(f"Moved from bottle {self.selected_bottle + 1} to bottle {bottle_index + 1}.")
                    else:
                        print_info("Invalid move.")
                self.selected_bottle = None

    def display_win_message(self):
        font = pygame.font.SysFont('Helvetica', 48)
        text = font.render("You Win!", True, (255, 255, 255))
        rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(text, rect)
        pygame.display.flip()

    def handle_quit(self):
        # Ask if the player wants to export the game using GUI
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
        """
        dialog_width = 400
        dialog_height = 150
        dialog_rect = pygame.Rect(
            (self.screen_width - dialog_width) // 2,
            (self.screen_height - dialog_height) // 2,
            dialog_width,
            dialog_height
        )

        yes_button = pygame.Rect(dialog_rect.left + 40, dialog_rect.bottom - 60, 100, 40)
        no_button = pygame.Rect(dialog_rect.right - 140, dialog_rect.bottom - 60, 100, 40)

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

            # Draw dialog background
            self.draw_rounded_rect(self.screen, (50, 50, 50), dialog_rect, 10)

            # Render text
            font = pygame.font.SysFont('Helvetica', 18)
            text_surface = font.render("Do you want to export the game?", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.screen_width // 2, dialog_rect.top + 50))
            self.screen.blit(text_surface, text_rect)

            # Draw buttons
            self.draw_button(yes_button, "Yes")
            self.draw_button(no_button, "No")

            pygame.display.flip()

        return False

    def show_filename_input(self):
        """
        Display a GUI input box to get the filename from the player.
        """
        dialog_width = 500
        dialog_height = 150
        dialog_rect = pygame.Rect(
            (self.screen_width - dialog_width) // 2,
            (self.screen_height - dialog_height) // 2,
            dialog_width,
            dialog_height
        )

        input_box = pygame.Rect(dialog_rect.left + 20, dialog_rect.centery - 20, dialog_width - 40, 40)
        input_text = ''
        active = True

        submit_button = pygame.Rect(dialog_rect.centerx - 50, dialog_rect.bottom - 50, 100, 40)

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

            # Draw dialog background
            self.draw_rounded_rect(self.screen, (50, 50, 50), dialog_rect, 10)

            # Prompt text rendering
            font = pygame.font.SysFont('Helvetica', 18)
            prompt_surface = font.render("Enter filename to export (e.g., game.csv):", True, (255, 255, 255))
            prompt_rect = prompt_surface.get_rect(midtop=(self.screen_width // 2, dialog_rect.top + 20))
            self.screen.blit(prompt_surface, prompt_rect)

            # Draw input box
            self.draw_rounded_rect(self.screen, (255, 255, 255), input_box, 5)
            if active:
                pygame.draw.rect(self.screen, (255, 215, 0), input_box, 2, border_radius=5)
            else:
                pygame.draw.rect(self.screen, (200, 200, 200), input_box, 2, border_radius=5)
            input_surface = font.render(input_text, True, (0, 0, 0))
            self.screen.blit(input_surface, (input_box.x + 5, input_box.y + 7))

            # Draw submit button
            self.draw_button(submit_button, "Save")

            pygame.display.flip()

        return None

    def draw_button(self, rect, text):
        """
        Draw a button with given rectangle and text.
        """
        # Draw button background
        self.draw_rounded_rect(self.screen, (70, 130, 180), rect, 5)
        # Draw button text
        font = pygame.font.SysFont('Helvetica', 18)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_rounded_rect(self, surface, color, rect, radius):
        """
        Draw a rectangle with rounded corners.
        """
        pygame.draw.rect(surface, color, rect, border_radius=radius)
