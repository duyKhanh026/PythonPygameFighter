from GUI.offline_2player import *
import socket
import json

class Player_client:
    def __init__(self, client, screen,  p1='', p2=''):
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.HEADER = 4096
        self.client = client
        self.getPlayer2 = False
        self.game = Offline_2player(screen, p1, p2)

    def send(self, msg):
        try:
            if msg == self.DISCONNECT_MESSAGE:
                self.client.sendall(json.dumps(self.DISCONNECT_MESSAGE).encode())
            else:
                self.client.sendall(json.dumps("pler/" + msg).encode())
            remessage = self.client.recv(4096).decode()
            print(remessage)
            if not remessage == 'NOPLAY':
                self.game.player2.from_string(remessage)
                if not self.getPlayer2:
                    if self.game.player2.name == 'Character 2':
                        self.game.player2 = Character2(800, 80, 'purple/stickman', 1100, 150, BLUE, None,   None,   None,   None,   None,   None, None, 'R')
                    if self.game.player2.name == 'Character 1':
                        self.game.player2 = Character1(800, 80, 'blue/stickman_blade', 1100, 150, BLUE, None,   None,   None,   None,   None,   None, None, 'R')

                    self.getPlayer2 = True

        except Exception as e:
            print("Error:", e)

    def run(self):
        while self.game.game_over == 0:
            self.game.run(True)
            self.send(str(self.game.player1))

        self.send(self.DISCONNECT_MESSAGE)