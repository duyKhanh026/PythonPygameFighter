from GUI.offline_2player import *
from GUI.client import Player_client
from GUI.Menu import Menu
from GUI.Lobby import WaitingRoom
from Values.values import *
import json

class Main: 
    def run(self):
        menu = Menu()
        while True:
            menu.run()
            # Vào game 2 người chơi 1 máy
            if menu.play_option == 1:
                offline_2player = Offline_2player(menu.screen)
                while offline_2player.retrunMenu == -1:
                    offline_2player.run()

            # Kết nối thông qua Lan
            if menu.play_option == 2:
                lobby = WaitingRoom(menu.screen)
                while lobby.option != 3:
                    lobby.run()
                lobby.client_socket.sendall(json.dumps("!DISCONNECT").encode())
                lobby.option = -1
            menu.play_option = -1

if __name__ == "__main__":
    Main().run()