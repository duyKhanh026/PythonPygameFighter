import json
import socket
import threading
from classes.player import Player
from classes.hostData import StringList

HEADER = 64
PORT = 5050
# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


my_string_list = StringList()
conns = []


def handle_client(conn, addr):
	print("[NEW CONNECTION] {addr} connected.")

	connected = True
	while connected:
		msg_length = conn.recv(HEADER).decode(FORMAT)
		if msg_length:
			msg_length = int(msg_length)
			msg = conn.recv(msg_length).decode(FORMAT)
			if msg == DISCONNECT_MESSAGE:
				my_string_list.remove_string(str(get_portt(addr)))
				connected = False

			# print(f"[{addr}] {msg}")
			senback = "NOPLAY"
			if connected:
				my_string_list.add_string(str(get_portt(addr)), msg)
				senback = my_string_list.get_coordinate(str(get_portt(addr)))
			conn.send(str(senback).encode(FORMAT))

	# conn.close()

def handle_room_client(conn, addr):
	print(f"[NEW ROOM CONNECTION] {addr} connected.")
	connected = True
	while connected:
		# Nhận dữ liệu từ client room
		msg = conn.recv(4096).decode(FORMAT)
		if msg:
			# Hiển thị dữ liệu nhận được từ client room
			print(f"[{addr}]: {msg}")
			data = json.loads(msg)
			if data == DISCONNECT_MESSAGE:
				my_string_list.remove_string(str(get_portt(addr)))
				connected = False
				break
			if extract_pler(str(data)) != None:
				# print(f"[{addr}] {msg}")
				my_string_list.add_pler(str(get_portt(addr)), extract_pler(str(data)))
				senback = my_string_list.get_coordinate(str(get_portt(addr)))
				conn.send(str(senback).encode(FORMAT))
			else :
				# Xử lý dữ liệu JSON
				try:
					# Thực hiện xử lý dữ liệu của room
					if extract_after_chat(str(data)) != None:
						chat = extract_after_chat(str(data))
						# conn.send(chat.encode(FORMAT))
						for connnn in conns:
							connnn.send(chat.encode(FORMAT))
					elif data != "Lobby connected":
						handle_room_data(data, addr)
						conn.send(str(my_string_list).encode(FORMAT))
					else:
						conn.send(str(my_string_list).encode(FORMAT))

				except json.JSONDecodeError as e:
					print(f"[ERROR] Invalid JSON format: {e}")

	conn.close()

def extract_after_chat(string):
	keyword = "chat/"
	index = string.find(keyword)
	if index != -1:
		return string[index + len(keyword):]
	else:
		return None

def extract_pler(string):
	keyword = "pler/"
	index = string.find(keyword)
	if index != -1:
		return string[index + len(keyword):]
	else:
		return None

def handle_room_data(data ,addr):
	# Xử lý dữ liệu của room ở đây
	room_code = data.get("code")
	room_name = data.get("name")
	room_player = data.get("player")
	print(f"Room Code: {room_code}, Name: {room_name}, Player: {room_player}")
	my_string_list.add_string(str(get_portt(addr)), str(room_name), str(room_player), 'tao ko bt', str(room_code))

def get_portt(adr):
	return adr[1]

def start():
	server.listen()
	print(f"[LISTENING] Server is listening on {SERVER}")
	while True:
		conn, addr = server.accept()
		conns.append(conn)
		thread1= threading.Thread(target=handle_room_client, args=(conn, addr))
		thread1.start()
		
		print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] server is starting...")
start()