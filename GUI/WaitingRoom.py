import pygame
import sys
import json
import threading
from client import Player_client

class WaitingRoom2:
    def __init__(self, surface, roomCode, client_socket, room_name):

        # Kích thước màn hình
        self.screen_width, self.screen_height = surface.get_size()
        self.roomCode = roomCode

        self.client_socket = client_socket
        self.room_name = room_name  # Lưu tên phòng chờ

        # Màu sắc
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.GREEN = (0, 255, 0)

        # Font cho văn bản
        self.font = pygame.font.Font(None, 24)
        self.font_name = pygame.font.Font(None, 48)

        # Tạo màn hình
        self.screen = surface

        # Tải hình nền
        self.background_image = pygame.image.load("GUI/background_waitingroom.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))
        self.char1show = pygame.transform.scale(pygame.image.load("assets/blue/stickman_blade_idle.png"), (640, 320))
        self.char2show = pygame.transform.scale(pygame.image.load("assets/purple/stickman_idle1wr.png"), (640, 320))

        # Khởi tạo danh sách các nhân vật
        self.characters = [
            Character("Character 1", self.char1show),
            Character("Character 2", self.char2show)
        ]

        # Danh sách người chơi
        self.players = [
            Player("Yasou", None)
        ]

        # Danh sách tin nhắn chat
        self.chat_messages = []

        # Tên phòng
        self.room_name_display = f"Room name: {self.room_name}"
        self.room_name_x = (self.screen_width - self.font_name.size(self.room_name_display)[0]) // 2

        # Biến lưu trữ nội dung tin nhắn đang nhập
        self.input_text = ""

        # Chạy vòng lặp chính
        self.running = True

        # Khởi tạo và bắt đầu luồng nhận tin nhắn
        self.message_receiver = MessageReceiver(self.client_socket, self.chat_messages)
        self.message_receiver.start()

        # Nút Exit
        self.exit_button_rect = pygame.Rect(20, 20, 100, 40)

    def draw_interface(self):
        # Vẽ hình nền
        self.screen.blit(self.background_image, (0, 0))

        # Vẽ tên phòng
        self.draw_text(self.room_name_display, self.font_name, self.WHITE, self.screen, self.room_name_x, 20)

        # Vẽ tên người chơi và các ô chọn nhân vật
        for i, player in enumerate(self.players):
            if player.name == "Yasou":
                self.draw_text(player.name, self.font_name, self.WHITE, self.screen, 150, 400)  # Điều chỉnh x và y tại đây
            elif player.name == "Leesin":
                self.draw_text(player.name, self.font_name, self.WHITE, self.screen, 1220, 400)  # Điều chỉnh x và y tại đây
            if player.character is not None:
                self.screen.blit(player.character.image, (-80 + i * 1100, 10))

        # Vẽ bảng chọn nhân vật
        for i, character in enumerate(self.characters):
            button_rect = pygame.Rect(520 + (i % 3) * 150, 100 + (i // 3) * 150, 120, 120)
            self.draw_text(character.name, self.font, self.WHITE, self.screen, 530 + (i % 3) * 150, 105 + (i // 3) * 150)
            character.button_rect = button_rect  # Lưu vị trí nút vào đối tượng nhân vật
            # Thu nhỏ hình ảnh nhân vật để vừa với nút
            scaled_image = pygame.transform.scale(character.image, (100, 100))
            image_x = button_rect.x + (button_rect.width - scaled_image.get_width()) // 2
            image_y = button_rect.y + (button_rect.height - scaled_image.get_height()) // 2
            self.screen.blit(scaled_image, (image_x, image_y))

        # Hiển thị đoạn chat
        chat_box_rect = pygame.Rect(20, 530, 1460, 150)
        pygame.draw.rect(self.screen, self.GRAY, chat_box_rect)

        # Hiển thị các tin nhắn chat
        for i, message in enumerate(self.chat_messages[-5:]):  # Hiển thị tối đa 5 tin nhắn cuối
            self.draw_text(message, self.font, self.WHITE, self.screen, 30, 540 + i * 30)

        # Vẽ hộp nhập liệu
        input_box_rect = pygame.Rect(20, 690, 1460, 40)
        pygame.draw.rect(self.screen, self.WHITE, input_box_rect)
        self.draw_text(self.input_text, self.font, self.BLACK, self.screen, 25, 700)

        # Vẽ nút Ready với bo tròn góc
        for i, player in enumerate(self.players):
            if player.name == "Yasou":
                ready_button_rect = pygame.Rect(150, 450, 100, 40)

            button_color = self.GREEN if player.ready else self.WHITE
            pygame.draw.rect(self.screen, button_color, ready_button_rect, border_radius=20)
            button_text = "All set" if player.ready else "Ready"
            self.draw_text(button_text, self.font, self.BLACK, self.screen, ready_button_rect.x + 10, ready_button_rect.y + 10)
            player.ready_button_rect = ready_button_rect  # Lưu vị trí nút vào đối tượng người chơi
            break

        # Vẽ nút Exit
        pygame.draw.rect(self.screen, self.WHITE, self.exit_button_rect, border_radius=20)
        self.draw_text("Exit", self.font, self.BLACK, self.screen, self.exit_button_rect.x + 25, self.exit_button_rect.y + 10)

        pygame.display.flip()

    def draw_text(self, text, font, color, surface, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_obj, text_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # self.leave_room()
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i, character in enumerate(self.characters):
                    if character.button_rect.collidepoint(mouse_pos):
                        self.players[0].character = self.characters[i]
                for player in self.players:
                    if player.ready_button_rect.collidepoint(mouse_pos):
                        player.ready = not player.ready
                # Xử lý sự kiện nhấn nút Exit
                if self.exit_button_rect.collidepoint(mouse_pos):
                    # self.leave_room()
                    self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # gửi đoạn chat đến server và server gửi lại chat
                    sendChat_message(self.input_text, self.client_socket)
                    self.input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode
        if self.players[0].ready:
            self.message_receiver.running = False
            self.client_socket.settimeout(1.0)
            Player_client(self.client_socket, self.screen,self.players[0].character.name, '').run()
            self.running = False

    
    def run(self):
        self.handle_events()
        if self.running:
            self.draw_interface()

#gửi tin nhắn từ client tới server thông qua một client socket đã được kết nối.
def sendChat_message(chat, client_socket):
    response = ""
    try:
        client_socket.sendall(json.dumps("chat/" + chat).encode())
    except Exception as e:
        print("Error:", e)
    return response

#nhận tin nhắn từ một client socket.
def receive_chat_message(client_socket):
    try:
        message = client_socket.recv(4096).decode()
        return message
    except client_socket.timeout:
        return None
    except Exception as e:
        return None

# tạo một luồng riêng biệt để nhận các tin nhắn từ một socket kết nối tới máy chủ. Bằng cách này, 
# việc nhận tin nhắn không cản trở luồng chính của ứng dụng, cho phép nó tiếp tục thực hiện các tác vụ khác 
# mà không bị chặn lại khi đang chờ đợi tin nhắn.
class MessageReceiver(threading.Thread):
    def __init__(self, client_socket, chat_messages):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.chat_messages = chat_messages
        self.running = True

    def run(self):
        while self.running:
            message = receive_chat_message(self.client_socket)
            if message:
                self.chat_messages.append(message)

class Player:
    def __init__(self, name, character):
        self.name = name
        self.character = character
        self.ready = False  # Trạng thái sẵn sàng của người chơi

class Character:
    def __init__(self, name, image):
        self.name = name
        self.image = image
