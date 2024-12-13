import math
import pygame as py
import numpy as np
import random
from classes.player import Player
from classes.character1 import Character1
from classes.character2 import Character2
from classes.action import *
from Values.values import *

class Game_play:
    def __init__(self, screen, online=False):
        self.game_over = 0
        self.screen = screen
        self.isOnline = online
        self.player1 = Character1(character1_folder, 300, 150, RED, py.K_a, py.K_d, py.K_w, py.K_g, py.K_h, py.K_j, py.K_e, 'L')
        self.player2 = Character1(character1_folder, 1100, 150, BLUE, py.K_LEFT, py.K_RIGHT, py.K_UP, py.K_b, py.K_n, py.K_m, py.K_p, 'R')

        self.settingBtn = py.image.load(f'assets/setting.png')
        self.settingClicked = True
        self.retrunMenu = -1
        self.infoMode = False
        self.notification = 'Choose the fighters to play.'
        self.playing = False
        self.clock = py.time.Clock()

    def setCharacter(self):
        p1_name = self.player1.name
        p2_name = self.player2.name
        if p1_name == 'Character 1':
            self.player1 = Character1(character1_folder, 300, 150, RED, py.K_a, py.K_d, py.K_w, py.K_g, py.K_h, py.K_j, py.K_e, 'L')
        else:
            self.player1 = Character2(character2_folder, 300, 150, RED, py.K_a, py.K_d, py.K_w, py.K_g, py.K_h, py.K_j, py.K_e, 'L')
        if self.isOnline:
            if p2_name == 'Character 2':
                self.player2 = Character2(character2_folder, 300, 150, BLUE, None,   None,   None,   None,   None,   None, None, 'R')
            else :
                self.player2 = Character1(character1_folder, 300, 150, BLUE, None,   None,   None,   None,   None,   None, None, 'R')
        else :
            if p2_name == 'Character 2':
                self.player2 = Character2(character2_folder, 1100, 150, BLUE, py.K_LEFT, py.K_RIGHT, py.K_UP, py.K_b, py.K_n, py.K_m, py.K_p, 'R')
            else :
                self.player2 = Character1(character1_folder, 1100, 150, BLUE, py.K_LEFT, py.K_RIGHT, py.K_UP, py.K_b, py.K_n, py.K_m, py.K_p, 'R')
        # đặt lại
        self.player1.name = p1_name
        self.player2.name = p2_name

        self.player1.tag_name = 'Fighter 1' if not self.isOnline else 'YOU' 
        self.player2.tag_name = 'Fighter 2' if not self.isOnline else 'OPPONENT'

        self.playing = True

    def reset(self):
        self.game_over = 0
        self.screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = py.time.Clock()
        self.setCharacter()

    # thực hiện xác nhận player thực hiện đánh thường hoặc đá
    def attack_confirmation(self, player, x, y):
        if player.attack_cooldown_p1 > 0:
            if self.infoMode: 
                draw_attack_cooldown(self.screen, player.attack_cooldown_p1, (x, y))
            player.attack_cooldown_p1 -= self.clock.get_time()
        elif player.state == 'ATK' or player.state == 'KIC':
            player.attack_ready_p1 = True
            player.attack_cooldown_p1 = 0
            player.state = 'NO'
        elif self.infoMode: 
            draw_attack_ready(self.screen, (x, y))

    # xác nhận player bị choáng
    def stunning_confirmation(self, player, x, y):
        if player.stunned_cooldown_p1 > 0:
            if self.infoMode: 
                draw_stunned_cooldown(self.screen, player.stunned_cooldown_p1, (x, y))
            player.stunned_cooldown_p1 -= self.clock.get_time()
        elif not player.stunned_ready_p1:
            player.stunned_ready_p1 = True
            player.JUMP_POWER = -15
        elif self.infoMode:
            draw_stunned_ready(self.screen, (x, y)) 

    # xác nhận player bị đá 
    def kicked_confirmation(self, player, x, y):
        if player.push_cooldown_p1 > 0:
            if self.infoMode: 
                draw_push_cooldown(self.screen, player.push_cooldown_p1, (x, y))
            player.push_cooldown_p1 -= self.clock.get_time()
        elif not player.push_ready_p1:
            player.push_ready_p1 = True
            player.state = 'NO'
        elif self.infoMode:
            draw_push_ready(self.screen, (x, y))

    # gán phía bị đẩy cho player
    def pushed_side(self, p1, p2):
        if p1.side == 'L':
            p2.state = 'PUS_R'  # đẩy về phía bên phải
        else:
            p2.state = 'PUS_L'  # đẩy về phía bên trái
    
    # xữ lý player2 khi player1 dùng đòn đá thành công
    def player_kick(self, p1, p2, online=False):
        if p1.state == 'KIC' and p2.state != 'ATK':
            if p1.kicAcount > 28 and p2.state != 'PUS_R' and p2.state != 'PUS_L':
                if handle_attack(p1, p2, online=online):
                    self.pushed_side(p1, p2)
                    p2.velocity_x = 8.4
                    p2.push_cooldown_p1 = PUSH_COOLDOWN
                    p2.push_ready_p1 = False

    # xữ lý player2 khi player1 dùng đòn đánh thường thành công
    def player_attack(self ,p1, p2, online=False):
        if p1.state == 'ATK' and p2.state != 'DEF':
            if p1.atkAcount == 16 and p2.state != 'STUN':
                if handle_attack(p1, p2, online=online):
                    p2.state = 'STUN'
                    p2.stunned_cooldown_p1 = STUNNED_COOLDOWN
                    p2.stunned_ready_p1 = False
                    p2.on_ground = False
                    self.pushed_side(p1, p2)
                    return True
        return False

    def backgr(self):
        self.screen.fill(GREEN1)

        py.draw.rect(self.screen, GRAY, (0, ground_height, SCREEN_WIDTH, ground_height))

        # # vẽ sọc trắng lên màn hình
        line_spacing = 50
        for y in range(0, SCREEN_HEIGHT, line_spacing):
            py.draw.line(self.screen, BLACK, (0, y), (SCREEN_WIDTH, y))
        line_spacing_vertical = 50
        for x in range(0, SCREEN_WIDTH, line_spacing_vertical):
            py.draw.line(self.screen, BLACK, (x, 0), (x, SCREEN_HEIGHT))

    def _update_ui(self):
        self.backgr()
        # gắn nút setting
        self.screen.blit(self.settingBtn, btn_setting)

        # xữ lý đầu vào để di chuyển và thực hiện hành động cho nhân vật 
        for player in [self.player1, self.player2]:
            if player == self.player1 or not self.isOnline:
                player.move_logic(py.key.get_pressed())
                player.sp_move(py.key.get_pressed())

            if player.state == 'ATK' or player.state == 'KIC':
                if player.attack_cooldown_p1 == 0:
                    player.attack_cooldown_p1 = ATTACK_COOLDOWN
                    player.attack_ready_p1 = False

            if player.skill_active(self.screen, self.player2 if player == self.player1 else self.player1):
                handle_attack(player, self.player2 if player == self.player1 else self.player1, True)
                self.pushed_side(player, self.player2 if player == self.player1 else self.player1)

            if player.rect.y > SCREEN_HEIGHT:
                self.game_over = (1 if player == self.player1 else 2) 
            elif player.health <= 0:
                self.game_over = (1 if player == self.player1 else 2) 

        self.attack_confirmation(self.player1, 10, toadoInfo)
        self.attack_confirmation(self.player2, SCREEN_WIDTH - 110, toadoInfo)

        self.player_attack(self.player1, self.player2, self.isOnline)
        self.player_attack(self.player2, self.player1)

        self.player_kick(self.player1, self.player2, self.isOnline)
        self.player_kick(self.player2, self.player1)

        self.stunning_confirmation(self.player1, 10, toadoInfo + 20)
        self.stunning_confirmation(self.player2, SCREEN_WIDTH - 110, toadoInfo + 20)

        self.kicked_confirmation(self.player1, 10, toadoInfo + 50)
        self.kicked_confirmation(self.player2, SCREEN_WIDTH - 110, toadoInfo + 50)

        if self.infoMode:
            for player in [self.player1, self.player2]:
                # Draw position info
                font = py.font.SysFont(None, 16)
                text = font.render(' (' + str(player.rect.x) + ',' + str(player.rect.y) + ')', True, (255, 255,255))
                self.screen.blit(text, (player.rect.x, 10))

                # Draw text about the current state 
                font = py.font.SysFont(None, 46)
                text = font.render(' ' + player.state, True, BLACK)
                self.screen.blit(text, (player.rect.x, player.rect.y + player.rect.height + 30))

                py.draw.line(self.screen, GREEN, (0, player.rect.y), (SCREEN_WIDTH, player.rect.y), 1)
                py.draw.line(self.screen, GREEN, (player.rect.x, 0), (player.rect.x, SCREEN_HEIGHT), 1)

    def _ui_setting(self):
        rect = py.Rect(300, 100, 900, 600)
        py.draw.rect(self.screen, BLACK, rect)
        py.draw.line(self.screen, WHITE, rect.topleft, rect.topright)
        py.draw.line(self.screen, WHITE, rect.topright, rect.bottomright)
        py.draw.line(self.screen, WHITE, rect.bottomright, rect.bottomleft)
        py.draw.line(self.screen, WHITE, rect.bottomleft, rect.topleft)

        font = py.font.SysFont(font_use, 32)

        # Phần cho thông báo
        text_surface = font.render("Notice: " + self.notification, True, WHITE)
        text_rect = text_surface.get_rect(topleft=(310, 105))
        self.screen.blit(text_surface, text_rect)

        text = font.render('fighter 1', True, WHITE)
        self.screen.blit(text, txt_fighter1)
        text = font.render('fighter 2', True, WHITE)
        self.screen.blit(text, txt_fighter2)

        self.draw_button('Go To Menu' , btn_gotomenu)
        self.draw_button("Infor ON" if self.infoMode else "Infor OFF" , btn_infor)
        self.draw_button("Resume" if self.playing else "PLAY!", btn_play)

        fighter = py.image.load(f'assets/{character1_folder}_idle1.png')
        self.screen.blit(fighter, btn_fighter1)
        self.screen.blit(fighter, (btn_fighter1[0] * 2.46, btn_fighter1[1]))
        fighter = py.image.load(f'assets/{character2_folder}_idle1.png')
        self.screen.blit(fighter, btn_fighter2)
        self.screen.blit(fighter, (btn_fighter1[0] * 2.46 + choice_box_size, btn_fighter1[1]))

        # Lựa chọn chọn fighter
        if self.player1.name != '':
            self.drawStyleRect(370 if self.player1.name == 'Character 1' else 370 + choice_box_size, 400)
        if self.player2.name != '':
            self.drawStyleRect(815 if self.player2.name == 'Character 1' else 815 + choice_box_size, 400)

        if self.isOnline:
            if self.player1.ready:
                text = font.render('Ready', True, GREEN)
                self.screen.blit(text, (txt_fighter1[0], txt_fighter1[1] + SCREEN_HEIGHT // 4))
            if self.player2.ready:
                text = font.render('Ready', True, GREEN)
                self.screen.blit(text, (txt_fighter2[0], txt_fighter2[1] + SCREEN_HEIGHT // 4))

    # Function to draw a button
    def draw_button(self, text, position):
        x, y = position
        font_button = py.font.SysFont(font_use, 24)
        py.draw.rect(self.screen, BUTTON_COLOR, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=20)
        text_surface = font_button.render(text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(x + BUTTON_WIDTH // 2, y + BUTTON_HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)

    def run(self):
        if self.game_over == 0:
            self._update_ui()
            for player in [self.player1, self.player2]:
                player.draw(self.screen)

            if self.game_over != 0:
                textEnd = "PLAYER 1 WIN" if self.game_over == 2 else "PLAYER 2 WIN"
                text = py.font.SysFont(None, 100).render(textEnd, True, BLUE)
                text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3))
                self.screen.blit(text, text_rect)

        if self.settingClicked: 
            self._ui_setting()

        self.clock.tick(60)
        py.display.update()

        if self.player1.name != '' and self.player2.name != '':
            if self.player1.ready and self.player2.ready:
                self.settingClicked = not self.settingClicked
                self.reset()
                if abs(self.player1.rect.x - self.player2.rect.x) <= 100:
                    self.player1.rect.x = random.randint(300, 1100)

        for event in py.event.get():
            if event.type == py.QUIT:
                self.game_over = -1
                if self.isOnline:
                    return
                else:
                    py.quit()
                    exit(1)
            elif event.type == py.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = py.mouse.get_pos()
                # Xử lý lúc nấn nút open/close setting
                if self.player1.name != '' and self.player2.name != '':
                    if self.playing:
                        if btn_setting[0] <= mouse_x <= (btn_setting[0] + box_setting):
                            if btn_setting[1] <= mouse_y <= (btn_setting[1] + box_setting):
                                self.settingClicked = not self.settingClicked
                                if self.game_over != 0:
                                    self.player1.name = ''  
                                    self.player2.name = ''
                                    self.playing = False

                if self.settingClicked:
                    if btn_play[0] <= mouse_x <= (btn_play[0] + BUTTON_WIDTH):
                        # Back to the Menu
                        if btn_gotomenu[1] <= mouse_y <= (btn_gotomenu[1] + BUTTON_HEIGHT):
                            self.retrunMenu = 1
                            self.game_over = -1
                        # Turn on/off information Mode
                        if btn_infor[1] <= mouse_y <= (btn_infor[1] + BUTTON_HEIGHT):
                            self.infoMode = not self.infoMode
                        # Back to the game
                        if self.player1.name != '' and self.player2.name != '':
                            if btn_play[1] <= mouse_y <= (btn_play[1] + BUTTON_HEIGHT):
                                if not self.playing or self.game_over != 0:
                                    if self.isOnline:
                                        self.player1.ready = True
                                    else:
                                        self.reset()
                                        self.settingClicked = not self.settingClicked
                        else :
                            self.notification = 'Not selected enough fighters.'

                    # Click to choice Fighter
                    if 400 <= mouse_y <= 555 and not self.playing:
                        if 370 <= mouse_x <= 370 + choice_box_size:
                            self.player1.name = 'Character 1'
                        if 525 < mouse_x <= 525 + choice_box_size:
                            self.player1.name = 'Character 2'
                        if not self.isOnline:
                            if 815 < mouse_x <= 815 + choice_box_size:
                                self.player2.name = 'Character 1'
                            if 970 < mouse_x <= 970 + choice_box_size:
                                self.player2.name = 'Character 2'

    def drawStyleRect(self, x, y):
        py.draw.rect(self.screen, YELLOW, (x,y,choice_box_size,choice_box_size), 1)
