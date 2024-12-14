import pygame
import os
import time
import socket
import json
from GUI.create_room import CreateRoomForm
from classes.hostData import StringList
from GUI.client import Player_client
from Values.values import *

class Lobby:
    def __init__(self, surface):
        self.screen = surface
        self.default_font_size = 30
        self.font_vietnamese = pygame.font.SysFont(font_use, self.default_font_size)

        # Tải hình ảnh nền
        self.background_image = pygame.image.load(menu_background)
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH - 240, SCREEN_WIDTH - 10))

        # Kích thước cửa sổ pygame
        self.window_width, self.window_height = surface.get_size()

        # Tính toán vị trí để cửa sổ xuất hiện ở giữa màn hình
        self.x_pos = (pygame.display.Info().current_w - self.window_width) // 2
        self.y_pos = (pygame.display.Info().current_h - self.window_height) // 2

        # Đặt vị trí cho cửa sổ
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{self.x_pos},{self.y_pos}"

        # Chọn font từ các font có sẵn trong hệ thống
        self.font_title = pygame.font.SysFont(font_use, 108)
        self.font_button = pygame.font.SysFont(font_use, 30)
        self.font_player = pygame.font.SysFont(font_use, 40)

        # Biến lưu trữ index của hàng được chọn
        self.selected_index = -1
        self.selected_room_code = None  # Biến lưu mã phòng đã chọn

        #biến cập nhật mỗi pid chỉ tạo 1 phòng
        self.room_created=False

        # alert
        self.show_alert=False

        # Server
        server_address=('127.0.0.1', 5050)
        self.server_address = server_address
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.server_address)

        self.room_list = []  # Danh sách phòng mẫu

        try:
            self.client_socket.sendall(json.dumps("Lobby connected").encode())

            # Nhận phản hồi từ server
            response = self.client_socket.recv(4096).decode()
            responSrlist = StringList()
            responSrlist.from_string(response)
            print(str(len(responSrlist.strings)))
            if responSrlist.strings[0] != "":
                for i in range(len(responSrlist.strings)):
                    new_room = {"name": responSrlist.name[i],
                                "players": str(responSrlist.player[i]), 
                                "code": responSrlist.code[i]}
                    
                    existing_room = next((room for room in self.room_list if room['code'] == new_room['code']), None)
                
                    if existing_room:
                        # Nếu mã code đã tồn tại, cập nhật giá trị players
                        existing_room['players'] = new_room['players']
                    else:
                        # Nếu mã code chưa tồn tại, thêm phòng mới vào danh sách
                        self.room_list.append(new_room)

        except Exception as e:
            print("Errorrrrrrrrrr:", e)

        self.scroll_pos = 0

        # Tính toán chiều cao của bảng
        self.table_height = SCREEN_HEIGHT - 155

        # Biến cờ để theo dõi trạng thái của việc nhấn chuột
        self.clicked = False
        self.option = -1

        # Tạo form create
        self.creating_room = False
    def draw_alert(self, message):
        # Kích thước và vị trí của hộp thông báo
        alert_width, alert_height = 400, 200
        alert_x = (SCREEN_WIDTH - alert_width) // 2
        alert_y = (SCREEN_HEIGHT - alert_height) // 2

        # Vẽ hộp thông báo
        pygame.draw.rect(self.screen, (255, 0, 0), (alert_x, alert_y, alert_width, alert_height), border_radius=20)
        pygame.draw.rect(self.screen, (255, 255, 255), (alert_x + 10, alert_y + 10, alert_width - 20, alert_height - 20), border_radius=20)

        # Vẽ nội dung thông báo
        alert_font = pygame.font.Font(self.font_path, 30)
        alert_text = alert_font.render(message, True, (0, 0, 0))
        alert_text_rect = alert_text.get_rect(center=(alert_x + alert_width // 2, alert_y + alert_height // 2))
        self.screen.blit(alert_text, alert_text_rect)

        # Vẽ nút "OK"
        ok_button = pygame.Rect(alert_x + alert_width // 2 - 50, alert_y + alert_height - 60, 100, 40)
        pygame.draw.rect(self.screen, (0, 255, 0), ok_button, border_radius=20)
        ok_text = alert_font.render("OK", True, (0, 0, 0))
        ok_text_rect = ok_text.get_rect(center=ok_button.center)
        self.screen.blit(ok_text, ok_text_rect)

        return ok_button

    # Hàm để vẽ một nút
    def draw_button(self, text, x, y):
        pygame.draw.rect(self.screen, BUTTON_COLOR, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=20)
        text_surface = self.font_button.render(text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(x + BUTTON_WIDTH // 2, y + BUTTON_HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)

    # Hàm để vẽ giao diện phòng chờ
    def draw_waiting_room(self):
        # Vẽ hình ảnh nền
        self.screen.blit(self.background_image, (0, 0))

        # Tiêu đề phòng chờ
        waiting_title = self.font_title.render("LOBBY", True, (255, 255, 255))
        title_rect = waiting_title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8))
        self.screen.blit(waiting_title, title_rect)

        # Tính toán kích thước của bảng
        table_width = SCREEN_WIDTH - 240

        # Vẽ bảng để hiển thị danh sách phòng
        table_rect = pygame.Rect(0, 150, table_width, self.table_height)
        pygame.draw.rect(self.screen, (255, 255, 255), table_rect, 2)  # Vẽ viền cho bảng

        # Tính toán số hàng hiển thị được
        num_visible_rows = min(self.table_height // 60, len(self.room_list))

        # Vẽ danh sách phòng dựa trên vị trí thanh cuộn
        start_index = self.scroll_pos
        end_index = min(self.scroll_pos + num_visible_rows, len(self.room_list))
        for i, room in enumerate(self.room_list[start_index:end_index], start=start_index):
            room_rect = pygame.Rect(table_rect.left + 10, table_rect.top + 10 + (i - start_index) * 60, table_width - 20, 50)

            # Kiểm tra xem chuột có hover trên hàng này không
            if room_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen, (220, 220, 220), room_rect)

            # Kiểm tra xem hàng này có phải là hàng được chọn không
            if self.selected_index == i:
                pygame.draw.rect(self.screen, (0, 255, 0), room_rect)  # Chọn màu xanh lá cây cho hàng được chọn

            # Vẽ thông tin phòng
            room_text_color = (255, 255, 255) if int(room['players']) < 2 else (150, 150, 150)  # Màu chữ phòng thay đổi khi có ít nhất 2 người chơi

            room_name_text = self.font_vietnamese.render(f"Room {i+1}: {room['name']}", True, room_text_color)
            player_count_text = self.font_vietnamese.render(f"{room['players']} / 2", True, room_text_color)

            room_name_text_rect = room_name_text.get_rect(left=room_rect.left , centery=room_rect.centery)
            player_count_text_rect = player_count_text.get_rect(right=room_rect.right - 10, centery=room_rect.centery)

            room_name_text_rect.width = room_rect.width * 1/3 - 10
            player_count_text_rect.width = room_rect.width * 1/3 - 10

            room_name_text_rect.right = room_name_text_rect.left + room_name_text_rect.width
            player_count_text_rect.left = player_count_text_rect.right - player_count_text_rect.width

            self.screen.blit(room_name_text, room_name_text_rect)
            self.screen.blit(player_count_text, player_count_text_rect)

            # Chỉ cho phép chọn phòng khi có ít hơn 2 người chơi
            if int(room['players']) < 2 and room_rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:  # Kiểm tra nút chuột trái được click hay không
                    print(f"Selected Room ID: {i+1}")
                    self.selected_index = i
                    self.selected_room_code = room['code']  # Lưu mã phòng đã chọn
                    time.sleep(0.2)  # Chờ 0.2s trước khi nhận input tiếp theo

        # Vẽ thanh cuộn
        scrollbar_rect = pygame.Rect(table_rect.right + 5, table_rect.top, 20, self.table_height)
        pygame.draw.rect(self.screen, (200, 200, 200), scrollbar_rect)
        if len(self.room_list) > 0:
            thumb_height = self.table_height / len(self.room_list) * num_visible_rows
            thumb_pos = self.scroll_pos / len(self.room_list) * self.table_height
            thumb_rect = pygame.Rect(scrollbar_rect.left + 5, scrollbar_rect.top + thumb_pos, 10, thumb_height)
            pygame.draw.rect(self.screen, (100, 100, 100), thumb_rect)

        self.draw_button("Join Room",   2.5 * (SCREEN_WIDTH // 3) + BUTTON_MARGIN, SCREEN_HEIGHT // 3)
        self.draw_button("Create Room", 2.5 * (SCREEN_WIDTH // 3) + BUTTON_MARGIN, SCREEN_HEIGHT // 3 + (BUTTON_HEIGHT + BUTTON_MARGIN))
        self.draw_button("Back",        2.5 * (SCREEN_WIDTH // 3) + BUTTON_MARGIN, SCREEN_HEIGHT // 3 + 2 * (BUTTON_HEIGHT + BUTTON_MARGIN))
        pygame.display.flip()

    def run(self):
        clicked = False
        self.draw_waiting_room()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # pygame.quit()
                self.option = 3
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5:  # Cuộn lên
                    if self.scroll_pos < len(self.room_list) - min(self.table_height // 60, len(self.room_list)):
                        self.scroll_pos = min(self.scroll_pos + 1, len(self.room_list) - min(self.table_height // 60, len(self.room_list)))
                elif event.button == 4:  # Cuộn xuống
                    if self.scroll_pos > 0:
                        self.scroll_pos = max(self.scroll_pos - 1, 0)
                elif event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Check which button the player clicked
                    if 2.34 * (SCREEN_WIDTH // 3) + BUTTON_MARGIN <= mouse_x <= 2.34 * (SCREEN_WIDTH // 3) + BUTTON_MARGIN + BUTTON_WIDTH:
                        if SCREEN_HEIGHT // 3 <= mouse_y <= SCREEN_HEIGHT // 3 + BUTTON_HEIGHT:
                            self.option = 1
                        if SCREEN_HEIGHT // 3 + (BUTTON_HEIGHT + BUTTON_MARGIN) <= mouse_y <= SCREEN_HEIGHT // 3 + (BUTTON_HEIGHT + BUTTON_MARGIN) + BUTTON_HEIGHT:
                            self.option = 2
                        if SCREEN_HEIGHT // 3 + 2 * (BUTTON_HEIGHT + BUTTON_MARGIN) <= mouse_y <= SCREEN_HEIGHT // 3 + 2 * (BUTTON_HEIGHT + BUTTON_MARGIN) + BUTTON_HEIGHT:
                            self.option = 3
                clicked = True

        if clicked and not pygame.mouse.get_pressed()[0]:
            clicked = False

        # Nút "Join Room"
        if self.option == 1:  
            if self.selected_room_code != None:
                # Lấy thông tin của phòng được chọn từ danh sách các phòng
                selected_room_name = next(room for room in self.room_list if room['code'] == self.selected_room_code)
                sp=int(selected_room_name['players']) + 1
                print(str(sp)+"......................")
                # Tăng số lượng người chơi trong phòng lên 1
                data = {
                    'code': self.selected_room_code,
                    'name': selected_room_name['name'],
                    'player': str(sp)
                }
                self.client_socket.send(json.dumps(data).encode())
                response = self.client_socket.recv(4096).decode()
                responSrlist = StringList()
                responSrlist.from_string(response)
                print(responSrlist.player[0]+" " + responSrlist.code[0] + " " + responSrlist.strings[0]+ " " + responSrlist.name[0])
                # Tăng số lượng người chơi trong phòng lên 1
                selected_room_name['players'] = str(data['player'])

                client_obj = Player_client(self.client_socket, self.screen)
                client_obj.run()
                if client_obj.codems == 1: # do mất chủ phòng
                    self.option = 4
                else :
                    self.option = 3

        # Nút "Create Room"
        elif self.option == 2:  
            if not self.room_created:
                self.creating_room = True  # Vẽ form nhập liệu
                self.room_created = True  # Cập nhật biến cờ sau khi tạo phòng
                self.option = -1
            else:
                self.show_alert = True  # Hiển thị thông báo
                self.alert_message = "This machine has already created a room."  # Nội dung thông báo
                self.option = -1

        # Nếu đang hiển thị form tạo phòng
        if self.creating_room:  
            create_room_form = CreateRoomForm(self.screen, self.client_socket)
            
            while create_room_form.option == 0:
                create_room_form.run()  # Vẽ form nhập liệu

            if create_room_form.option == 1:
                Player_client(self.client_socket, self.screen, True).run()
                self.option=3
                self.creating_room = False
            else :
                self.creating_room = False
                self.room_created = False