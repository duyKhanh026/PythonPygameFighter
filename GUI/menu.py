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

        # Tải hình ảnh nền
        self.background_image = pygame.image.load(menu_background)
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Select a font from the available fonts in the system
        self.font_title = pygame.font.SysFont(font_use, 72)
        self.font_button = pygame.font.SysFont(font_use, 24)

        self.notification = ''

        self.btnPlayOffline = pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) // 2, 
            SCREEN_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.btnPlayOnline = pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) // 2, 
            SCREEN_HEIGHT // 2 + BUTTON_HEIGHT + BUTTON_MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.btnExit = pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) // 2, 
            SCREEN_HEIGHT // 2 + (BUTTON_HEIGHT + BUTTON_MARGIN) * 2, BUTTON_WIDTH, BUTTON_HEIGHT)

    # Function to draw a button
    def draw_button(self, text, btn):
        pygame.draw.rect(self.screen, BUTTON_COLOR, btn, border_radius=20)
        text_surface = self.font_button.render(text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(btn.x + BUTTON_WIDTH // 2, btn.y + BUTTON_HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)

    # Function to draw the menu interface
    def draw_menu(self):
        # Draw background image
        self.screen.blit(self.background_image, (0, 0))

        # Game title
        game_title = self.font_title.render(game_name, True, (255, 255, 255))
        title_rect = game_title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(game_title, title_rect)
        # Draw buttons
        self.draw_button("Play 2 Players", self.btnPlayOffline)
        self.draw_button("LAN", self.btnPlayOnline)
        self.draw_button("Exit", self.btnExit)
        
        # Phần cho thông báo
        text_surface = self.font_button.render("Notice: " + self.notification, True, WHITE)
        text_rect = text_surface.get_rect(topleft=(10, 5))
        self.screen.blit(text_surface, text_rect)

        pygame.display.flip()

    # Main function
    def run(self):
        self.draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Select play game
                if self.btnPlayOffline.collidepoint(event.pos):
                    self.play_option = 1
                # Select play online
                elif self.btnPlayOnline.collidepoint(event.pos):
                    self.play_option = 2
                # Quit
                elif self.btnExit.collidepoint(event.pos):
                    pygame.quit()
                    exit(1)