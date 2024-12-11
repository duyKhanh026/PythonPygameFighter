import pygame
import sys
import subprocess

# Khởi tạo Pygame
pygame.init()

# Các màu cơ bản
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Kích thước cửa sổ
SCREEN_WIDTH = 994
SCREEN_HEIGHT = 705

# Khởi tạo cửa sổ
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Đối Kháng")

# Liệt kê các font có sẵn
available_fonts = pygame.font.get_fonts()
print("Available fonts:", available_fonts)

# Chọn font chữ
font_name = "timesnewroman"  # Chọn một tên font chữ từ danh sách các font có sẵn
font_size = 48
font = pygame.font.SysFont(font_name, font_size)

# Hiển thị màn hình chào mừng
def intro_screen():
    screen.fill(BLACK)
    title_text = font.render("Welcome to my game", True, YELLOW)
    
    # Vị trí ban đầu của chữ
    title_rect = title_text.get_rect(left=-SCREEN_WIDTH, centery=SCREEN_HEIGHT//2)
    
    clock = pygame.time.Clock()  # Đồng hồ để giới hạn tốc độ khung hình
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return "menu"

        # Di chuyển chữ từ trái sang phải
        title_rect.x += 2
        
        # Vẽ chữ lên màn hình
        screen.fill(BLACK)
        screen.blit(title_text, title_rect)
        pygame.display.flip()
        
        # Giới hạn tốc độ khung hình
        clock.tick(120)

        # Kết thúc vòng lặp nếu chữ đã di chuyển qua màn hình
        if title_rect.left >= SCREEN_WIDTH:
            running = False

    # Trả về màn hình menu sau khi chữ chạy xong
    return "menu"

# Màn hình menu
def menu_screen():
    # Khởi chạy file Menu.py
    subprocess.Popen(["python", "GUI\Menu.py"])
    pygame.quit()
    sys.exit()

# Hàm main
def main():
    next_screen = "intro"
    while True:
        if next_screen == "intro":
            next_screen = intro_screen()
        elif next_screen == "menu":
            menu_screen()
            

# Chạy trò chơi
if __name__ == "__main__":
    main()
