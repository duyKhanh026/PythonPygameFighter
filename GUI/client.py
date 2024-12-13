import json
import socket
from Values.values import *
from GUI.game_play import *

class Player_client:
    def __init__(self, client, screen):
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.HEADER = 4096
        self.client = client
        self.game = Game_play(screen, True)

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

        except Exception as e:
            print("Error:", e)

    def run(self):
        while self.game.game_over == 0 and self.game.retrunMenu == -1:
            self.game.run()
            self.send(str(self.game.player1))

        self.send(self.DISCONNECT_MESSAGE)