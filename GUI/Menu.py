import sys
import pygame
from Values.values import *

class Menu:
    def __init__(self):
        # Khởi tạo Pygame
        self.play_option = -1
        pygame.init()
        # Khởi tạo cửa sổ
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(game_name)

        # Kích thước cửa sổ pygame
        self.window_width, self.window_height = self.screen.get_size()

        # Tải hình ảnh nền
        self.background_image = pygame.image.load(menu_background)
        self.background_image = pygame.transform.scale(self.background_image, (self.window_width, self.window_height))

        # Select a font from the available fonts in the system
        self.font_title = pygame.font.SysFont(font_use, 72)
        self.font_button = pygame.font.SysFont(font_use, 24)

        # Button dimensions and colors
        self.BUTTON_WIDTH = 200
        self.BUTTON_HEIGHT = 40
        self.BUTTON_MARGIN = 40  # Increased margin between buttons
        self.BUTTON_COLOR = WHITE
        self.BUTTON_TEXT_COLOR = BLACK

    # Function to draw a button
    def draw_button(self, text, x, y):
        pygame.draw.rect(self.screen, self.BUTTON_COLOR, (x, y, self.BUTTON_WIDTH, self.BUTTON_HEIGHT), border_radius=20)
        text_surface = self.font_button.render(text, True, self.BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(x + self.BUTTON_WIDTH // 2, y + self.BUTTON_HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)

    # Function to draw the menu interface
    def draw_menu(self):
        # Draw background image
        self.screen.blit(self.background_image, (0, 0))

        # Game title
        game_title = self.font_title.render("Fighting Game", True, (255, 255, 255))
        title_rect = game_title.get_rect(center=(self.window_width // 2, self.window_height // 3))
        self.screen.blit(game_title, title_rect)
        # Draw buttons
        self.draw_button("Play 2 Players", (self.window_width - self.BUTTON_WIDTH) // 2, self.window_height // 2)
        self.draw_button("LAN", (self.window_width - self.BUTTON_WIDTH) // 2, self.window_height // 2 + self.BUTTON_HEIGHT + self.BUTTON_MARGIN)
        pygame.display.flip()

    # Main function
    def run(self):
        self.draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check which button the player clicked
                if (self.window_width - self.BUTTON_WIDTH) // 2 <= mouse_x <= (self.window_width - self.BUTTON_WIDTH) // 2 + self.BUTTON_WIDTH:
                    if self.window_height // 2 <= mouse_y <= self.window_height // 2 + self.BUTTON_HEIGHT:
                        # print("Play with Bot") 
                        self.play_option = 1
                    elif self.window_height // 2 + self.BUTTON_HEIGHT + self.BUTTON_MARGIN <= mouse_y <= self.window_height // 2 + 2 * (self.BUTTON_HEIGHT + self.BUTTON_MARGIN):
                        # print("Play 2 Players")
                        self.play_option = 2
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    # Change player name when 'n' key is pressed
                    self.player_name = input("Enter player name: ")