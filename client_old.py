import pygame as py
import socket
import re
from classes.player import Player
from classes.action import *
from values.color import *
from values.screen import *

class Player_client:
    def __init__(self, server_ip="127.0.0.1", port=5050):
        self.SERVER = server_ip
        self.PORT = port
        self.FORMAT = 'utf-8'
        self.HEADER = 64
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.ADDR = (self.SERVER, self.PORT)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)

        py.init()

        self.screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        py.display.set_caption('Demo')

        self.player1 = Player(200, 50, 'blue/stickman_blade', 300, 150,  RED, py.K_a, py.K_d, py.K_w, py.K_g, py.K_h, py.K_j, py.K_e, 'L',)
        self.player2 = Player(200, 70, 'purple/stickman', 1200, -150, BLUE,   None,   None,   None,   None,   None,   None, None, 'R')
        self.player2.on_ground = True

    def send(self, msg):
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
        remessage = self.client.recv(2048).decode(self.FORMAT)
        if not remessage == 'NOPLAY':
            self.player2.from_string(remessage)
            print(remessage)

    def run(self):
        run = True
        clock = py.time.Clock()

        while run:
            self.screen.fill(BLACK)

            line_spacing = 50
            for y in range(0, SCREEN_HEIGHT, line_spacing):
                py.draw.line(self.screen, WHITE, (0, y), (SCREEN_WIDTH, y))

            line_spacing_vertical = 50
            for x in range(0, SCREEN_WIDTH, line_spacing_vertical):
                py.draw.line(self.screen, WHITE, (x, 0), (x, SCREEN_HEIGHT))

            for player in [self.player1, self.player2]:
                player.move_logic(py.key.get_pressed())
                player.sp_move(py.key.get_pressed())
                player.draw(self.screen)

                if player.state == 'ATK' or player.state == 'KIC':
                    if player.attack_cooldown_p1 == 0:
                        player.attack_cooldown_p1 = ATTACK_COOLDOWN
                        player.attack_ready_p1 = False

            for player in [self.player1, self.player2]:
                if player.attack_cooldown_p1 > 0:
                    draw_attack_cooldown(self.screen, player.attack_cooldown_p1, (10 if player == self.player1 else SCREEN_WIDTH - 110, 30))
                    player.attack_cooldown_p1 -= clock.get_time()
                elif player.state == 'ATK' or player.state == 'KIC':
                    player.attack_ready_p1 = True
                    player.attack_cooldown_p1 = 0
                    player.state = 'NO'
                else: 
                    draw_attack_ready(self.screen, (10 if player == self.player1 else SCREEN_WIDTH - 110, 30))

            if check_collision(self.player1, self.player2):
                for player in [self.player1, self.player2]:
                    if player != self.player1 and player.state == 'KIC' and (self.player2.state if player == self.player1 else self.player1.state) != 'ATK':
                        if player.kicAcount > 30 and (self.player2.state if player == self.player1 else self.player1.state) != 'PUS':
                            handle_attack(self.player1 if player == self.player1 else self.player2, self.player2 if player == self.player1 else self.player1)
                            if player == self.player1: 
                                self.player2.state = 'PUS' 
                            else: 
                                self.player1.state = 'PUS'

                            if player == self.player1:
                                self.player2.push_cooldown_p1 = PUSH_COOLDOWN
                            else:
                                self.player1.push_cooldown_p1 = PUSH_COOLDOWN

                            if player == self.player1:
                                self.player2.push_ready_p1 = False
                            else:
                                self.player1.push_ready_p1 = False

                if self.player2.state == 'ATK' and self.player1.state != 'DEF':
                    if self.player2.atkAcount > 16 and self.player1.state != 'STUN':
                        handle_attack(self.player2, self.player1)
                        self.player1.state = 'STUN'  
                        self.player1.stunned_cooldown_p1 = STUNNED_COOLDOWN
                        self.player1.stunned_ready_p1 = False

            for player in [self.player1, self.player2]:
                if player.stunned_cooldown_p1 > 0:
                    draw_stunned_cooldown(self.screen, player.stunned_cooldown_p1, (10 if player == self.player1 else SCREEN_WIDTH - 110, 50))
                    player.stunned_cooldown_p1 -= clock.get_time()
                elif not player.stunned_ready_p1:
                    player.stunned_ready_p1 = True
                    player.state = 'NO'
                else:
                    draw_stunned_ready(self.screen, (10 if player == self.player1 else SCREEN_WIDTH - 110, 50)) 

            for player in [self.player2, self.player1]:
                if player.push_cooldown_p1 > 0:
                    draw_push_cooldown(self.screen, player.push_cooldown_p1, (10 if player == self.player1 else SCREEN_WIDTH - 110, 80))
                    player.push_cooldown_p1 -= clock.get_time()
                elif not player.push_ready_p1:
                    player.push_ready_p1 = True
                    player.state = 'NO'
                else:
                    draw_push_ready(self.screen, (10 if player == self.player1 else SCREEN_WIDTH - 110, 80))

            for event in py.event.get():
                if event.type == py.QUIT:
                    run = False

            py.display.update()
            clock.tick(60)

            self.send(str(self.player1))

        py.quit()
        self.send(self.DISCONNECT_MESSAGE)
