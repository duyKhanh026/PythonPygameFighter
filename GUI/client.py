import json
import socket
from Values.values import *
from GUI.game_play import *

class Player_client:
    def __init__(self, client, screen, own_room=False):
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.HEADER = 4096
        self.client = client
        self.opn_has_entered = False
        self.own_room = own_room
        self.game = Game_play(screen, True, own_room=self.own_room)
        self.codems = 0

    def send(self, msg):
        try:
            if msg == self.DISCONNECT_MESSAGE:
                self.client.sendall(json.dumps(msg).encode())
            else:
                self.client.sendall(json.dumps("pler/" + msg).encode())
            remessage = self.client.recv(4096).decode()
            # print(remessage)
            if not remessage == 'NOPLAY':
                self.game.player2.from_string(remessage)
                self.opn_has_entered = True
                if self.own_room:
                    self.game.notification = "Opponent has connected."

            elif self.opn_has_entered: 
                if self.own_room:
                    self.game.player2.name = ''
                    self.game.settingClicked = True
                    self.game.playing = False
                    self.game.notification = "The opponent has lost connection."
                    self.opn_has_entered = False
                else:
                    self.codems = 1 # code nhận bt chủ phòng đã rời đi
                    self.game.retrunMenu = 1
        except Exception as e:
            print("Error:", e)

    def run(self):
        while self.game.retrunMenu == -1 and self.codems == 0:
            self.game.run()
            self.send(str(self.game.player1))
        self.send(self.DISCONNECT_MESSAGE)