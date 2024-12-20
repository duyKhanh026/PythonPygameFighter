import random
import pygame
from classes.room import Room,RoomClient
from classes.hostData import StringList
from Values.values import *

class CreateRoomForm:
    def __init__(self, surface, client):
        self.screen = surface
        self.client = client

        # Kích thước và vị trí của form, ô nhập liệu và nút
        self.FORM_WIDTH = 400
        self.FORM_HEIGHT = 200
        self.FORM_X = (SCREEN_WIDTH - self.FORM_WIDTH) // 2
        self.FORM_Y = (SCREEN_HEIGHT - self.FORM_HEIGHT) // 2
        self.INPUT_WIDTH = 300
        self.INPUT_HEIGHT = 30
        self.BUTTON_WIDTH = 100
        self.BUTTON_HEIGHT = 40
        self.BUTTON_MARGIN = 20

        # Font chữ
        self.font = pygame.font.Font(None, 30)

        # Text
        self.input_text = "default"

        # Tạo các hình chữ nhật cho form, ô nhập liệu và nút
        self.form_rect = pygame.Rect(self.FORM_X, self.FORM_Y, self.FORM_WIDTH, self.FORM_HEIGHT)
        self.input_rect = pygame.Rect(self.FORM_X + (self.FORM_WIDTH - self.INPUT_WIDTH) // 2,
                                      self.FORM_Y + 60, self.INPUT_WIDTH, self.INPUT_HEIGHT)
        self.create_button_rect = pygame.Rect(self.FORM_X + (self.FORM_WIDTH - self.BUTTON_WIDTH * 2 - self.BUTTON_MARGIN) // 2,
                                              self.FORM_Y + 120, self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        self.cancel_button_rect = pygame.Rect(self.FORM_X + (self.FORM_WIDTH + self.BUTTON_MARGIN) // 2,
                                              self.FORM_Y + 120, self.BUTTON_WIDTH, self.BUTTON_HEIGHT)

        self.responStrLs = StringList()
        self.option = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.create_button_rect.collidepoint(mouse_pos):
                        room= Room(self.generate_room_code(),self.input_text,1)
                        roomclient= RoomClient(self.client)
                        self.responStrLs = roomclient.create_room(room)
                        self.option = 1
                    elif self.cancel_button_rect.collidepoint(mouse_pos):
                        self.option = 2
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode

    def draw(self):
        # Vẽ form
        pygame.draw.rect(self.screen, WHITE1, self.form_rect)

        # Vẽ label "Name"
        label_surface = self.font.render("Name:", True, BLACK)
        label_rect = label_surface.get_rect(topleft=(self.FORM_X + 50, self.FORM_Y + 30))
        self.screen.blit(label_surface, label_rect)

        # Vẽ ô nhập liệu
        pygame.draw.rect(self.screen, WHITE, self.input_rect)
        input_surface = self.font.render(self.input_text, True, BLACK)
        input_rect = input_surface.get_rect(midleft=(self.input_rect.x + 10, self.input_rect.centery))
        self.screen.blit(input_surface, input_rect)

        # Vẽ nút "Create"
        pygame.draw.rect(self.screen, GRAY2, self.create_button_rect)
        create_surface = self.font.render("Create", True, BLACK)
        create_rect = create_surface.get_rect(center=self.create_button_rect.center)
        self.screen.blit(create_surface, create_rect)

        # Vẽ nút "Cancel"
        pygame.draw.rect(self.screen, GRAY2, self.cancel_button_rect)
        cancel_surface = self.font.render("Cancel", True, BLACK)
        cancel_rect = cancel_surface.get_rect(center=self.cancel_button_rect.center)
        self.screen.blit(cancel_surface, cancel_rect)

        pygame.display.flip()

    # generate code
    def generate_room_code(self):
        # Tạo mã phòng ngẫu nhiên
        return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
    
    
    def run(self):
        self.handle_events()
        self.draw() 