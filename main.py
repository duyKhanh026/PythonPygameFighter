from GUI.game_play import *
from GUI.client import Player_client
from GUI.menu import Menu
from GUI.lobby import Lobby
from Values.values import *
import json

class Main: 
    def run(self):
        menu = Menu()

        while True:
            menu.run()
            # Vào game 2 người chơi 1 máy
            if menu.play_option == 1:
                offline_2player = Game_play(menu.screen)
                while offline_2player.retrunMenu != 1:
                    offline_2player.run()

            # Kết nối thông qua Lan
            if menu.play_option == 2:
                try:
                    lobby = Lobby(menu.screen)
                    while lobby.option != 3:
                        lobby.run()
                    lobby.client_socket.sendall(json.dumps("!DISCONNECT").encode())
                    lobby.option = -1
                except:
                    menu.notification = 'Server not found'
                
            menu.play_option = -1

if __name__ == "__main__":
    Main().run()