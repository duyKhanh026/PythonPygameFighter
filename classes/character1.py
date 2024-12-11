import pygame as py
from classes.player import Player

class Character1(Player): # the blue guy 
	def __init__(self, hx, hy, strNam, x, y, color, move_left_key, move_right_key, jump_key, atk_key, def_key, kick_key, sp1_key, side):
		super().__init__(hx, hy, strNam, x, y, color, move_left_key, move_right_key, jump_key, atk_key, def_key, kick_key, sp1_key, side)
		self.sp1 = [py.image.load(f'assets/{strNam}_sp{i}.png') for i in range(1, 20)]
		self.image1 = py.image.load("assets/kill1.png")
		self.hinh_1_list = []
		self.lengt = int(600 / 50)
		self.startX = 0

		# Thêm 10 biến hình 1 vào list
		for i in range(0, self.lengt):
			self.hinh_1_list.append(self.image1)
		self.spam = False
		self.spam_l = 0
		self.frame_count = 0
		self.frame_rate = 3

	def redrawGameWindow(self, surface):
		if self.walkCount + 1 >= 30: # 5frame
			self.walkCount = 0
		if self.kicAcount + 1 >= 42: # 7frame
			self.kicAcount = 0
		if self.sp1count + 1 >= 114: # 19 frame
			self.skill1 = True
			self.sp1count = 113
		if self.idlecount >= 30:
			self.idlecount = 0

		if self.state != 'NO':
			self.moveEnable = False
		else :
			self.moveEnable = True
			
		if self.state == 'SP1':
			surface.blit(self.sp1[self.sp1count//6] if self.side == 'L' else py.transform.flip(self.sp1[self.sp1count//6], True, False), (self.rect.x - self.rect.width, self.rect.y - 100))
			if self.sp1count < 113:
				self.sp1count += 1
		else :
			return super().redrawGameWindow(surface)

	def skill_use(self, surface, player2):
		if not self.skill1:
			self.spam_l = self.lengt
			self.startX = self.rect.x + self.rect.width
			return False
		# Vẽ hình 1
		for i in range(0, self.lengt - self.spam_l):
			if self.side == 'L':
				x = self.startX + i * 50
			else: 
				x = (self.startX - self.rect.width - 50) - i * 50
			y = self.rect.y
			objA = py.Rect(x, y, 50, 150)
			surface.blit(self.hinh_1_list[i], (x, y))
			if (objA.colliderect(player2.rect)):
				player2.get_hit_by_skill = True

		# Cập nhật mỗi 10 fps
		self.frame_count += 1
		if self.frame_count % 3 == 0 and self.spam_l > 0 :
			self.spam_l -= 1

		if self.frame_count == 100:
			self.frame_count = 0
			self.spam_l = self.lengt 
			return True

	def skill_active(self, screen, player2):
		if self.skill_use(screen, player2): 
			self.skill1 = False
			self.state = 'NO'
			self.sp1count = 0

		if player2.get_hit_by_skill :
			player2.JUMP_POWER = -10 - (100 - player2.health) / 7
			player2.velocity_x = 10 + (100 - player2.health) / 7
			player2.square_y_speed = player2.JUMP_POWER
			player2.on_ground = False
			player2.get_hit_by_skill = False
			return True
		player2.JUMP_POWER = -15
		return False