import pygame as py

class Player:
	def __init__(self, hx, hy, strNam, x, y, color, move_left_key, move_right_key, jump_key, atk_key, def_key, kick_key, sp1_key, side):
		self.health_bar_x = hx
		self.health_bar_y = hy
		self.name = ''
		self.hitbox = 100
		self.right = False
		self.left = False
		self.Max_jump = 2
		self.click_jump_enable = True
		self.load_images(strNam)
		self.set_starting_parameters(x, y, color, side)
		self.set_control_keys(move_left_key, move_right_key, jump_key, atk_key, def_key, kick_key, sp1_key)
		self.set_default_values()
		self.key_twice = 10
		self.moveEnable = True

	def load_images(self, strNam):
		self.walkRight = [py.image.load(f'assets/{strNam}_running{i}.png') for i in range(1, 6)]
		self.slashA1 = [py.image.load(f'assets/{strNam}_slash{i}.png') for i in range(1, 5)]
		self.kickA = [py.image.load(f'assets/{strNam}_kick{i}.png') for i in range(1, 8)]
		self.charIdle = [py.image.load(f'assets/{strNam}_idle{i}.png') for i in range(1, 6)]
		self.defenseA = py.image.load(f'assets/{strNam}_defense.png')

	def set_starting_parameters(self, x, y, color, side):
		self.rect = py.Rect(x, y, 100, 150)
		self.color = color
		self.side = side
		self.max_health = 100
		self.health = self.max_health

	def set_control_keys(self, move_left_key, move_right_key, jump_key, atk_key, def_key, kick_key, sp1_key):
		self.move_left_key = move_left_key
		self.move_right_key = move_right_key
		self.jump_key = jump_key
		self.atk_key = atk_key
		self.def_key = def_key
		self.kick_key = kick_key
		self.sp1_key = sp1_key

	def set_default_values(self):
		self.speed = 6
		self.GRAVITY = 0.5
		self.sp1count = 0
		self.walkCount = 0
		self.atkAcount = 0
		self.kicAcount = 0
		self.idlecount = 0
		self.velocity_x = 0
		self.JUMP_POWER = -15
		self.square_y_speed = 0
		self.push_cooldown_p1 = 0
		self.attack_cooldown_p1 = 0
		self.stunned_cooldown_p1 = 0
		self.skill1 = False
		self.on_ground = False
		self.push_ready_p1 = True
		self.attack_ready_p1 = True
		self.stunned_ready_p1 = True
		self.get_hit_by_skill = False
		self.state = 'NO'

	def redrawGameWindow(self, surface):
		if self.state == 'ATK':
			if self.atkAcount < 23:
				self.atkAcount += 1
			elif self.atkAcount > 23:
				self.atkAcount = 0
			surface.blit(self.slashA1[self.atkAcount//6] if self.side == 'L' else py.transform.flip(self.slashA1[self.atkAcount//6], True, False), (self.rect.x - self.rect.width, self.rect.y - 100))
		elif self.state == 'KIC':
			surface.blit(self.kickA[self.kicAcount//6] if self.side == 'L' else py.transform.flip(self.kickA[self.kicAcount//6], True, False), (self.rect.x - self.rect.width, self.rect.y))
			self.kicAcount += 1
		elif self.right:
			surface.blit(self.walkRight[self.walkCount//6], (self.rect.x - self.rect.width, self.rect.y))
			self.walkCount += 1
		elif self.left:
			surface.blit(py.transform.flip(self.walkRight[self.walkCount//6], True, False), (self.rect.x - self.rect.width, self.rect.y))
			self.walkCount += 1
		elif self.state == 'DEF':
			surface.blit(self.defenseA if self.side == 'L' else py.transform.flip(self.defenseA, True, False), (self.rect.x - self.rect.width, self.rect.y))
		else :
			surface.blit(self.charIdle[self.idlecount//6] if self.side == 'L' else py.transform.flip(self.charIdle[self.idlecount//6], True, False), (self.rect.x - self.rect.width, self.rect.y - self.rect.height + 50))
			self.idlecount += 1

	def move(self, dx, dy):
		self.rect.move_ip(dx, dy)

	def draw(self, surface):
		# py.draw.rect(surface, self.color, self.rect)
		# if self.side == 'L':
		# 	py.draw.rect(surface, self.color, py.Rect(self.rect.x + self.hitbox,self.rect.y, 100,100))
		# else:
		# 	py.draw.rect(surface, self.color, py.Rect(self.rect.x - self.hitbox,self.rect.y, 100,100))

		self.redrawGameWindow(surface)
		# py.draw.line(surface, (26, 243, 0), (self.rect.x, 0), (self.rect.x, 800))
		# py.draw.line(surface, (26, 243, 0), (0, self.rect.y), (1500, self.rect.y))
		font = py.font.SysFont(None, 16)
		text = font.render(' (' + str(self.rect.x) + ',' + str(self.rect.y) + ')', True, (255, 255,255))
		surface.blit(text, (self.rect.x, 10))

		# Draw health bar
		py.draw.rect(surface, (255, 0, 0), (self.health_bar_x, self.health_bar_y, self.rect.width, 10))
		py.draw.rect(surface, (0, 255, 0), (self.health_bar_x, self.health_bar_y, int(self.rect.width * (self.health / self.max_health)), 10))
		
		# Draw text about the current state 
		font = py.font.SysFont(None, 46)
		text = font.render(' ' + self.state, True, (255, 255,255))
		surface.blit(text, (self.rect.x, self.rect.y + self.rect.height // 2))

	def go_left(self):
		self.right = False
		self.side = 'R'
		self.left = True
		self.move(-self.speed, 0)

	def go_right(self):
		self.right = True
		self.side = 'L'
		self.left = False
		self.move(self.speed, 0)

	def do_jump(self):
		self.square_y_speed = self.JUMP_POWER
		self.on_ground = False
		self.Max_jump -= 1
		self.click_jump_enable = False

	def do_atk(self):
		self.atkAcount = 0
		self.state = 'ATK'

	def do_kic(self):
		self.kicAcount = 0
		self.state = 'KIC'

	def do_def(self):
		self.state = 'DEF'


	def sp_move(self, key):
		if self.move_left_key == None:
			return 

		if key[self.sp1_key] and not self.skill1:
			self.state = 'SP1'
			self.sp1count = 0
		elif self.state == 'DEF' or self.state == 'NO':
			if key[self.atk_key]:
				self.atkAcount = 0
				self.state = 'ATK'
			elif key[self.def_key]:
				self.state = 'DEF'
			elif key[self.kick_key]:
				self.kicAcount = 0
				self.state = 'KIC'
			else:
				self.state = 'NO'

	def move_logic(self, key):
		# Áp dụng trọng lực
		# if not self.on_ground or self.rect.y >= 600 - self.rect.height:
		self.square_y_speed += self.GRAVITY
		self.rect.y += self.square_y_speed

		

		# Kiểm tra va chạm với mặt đất ma
		if self.rect.x > 150 and self.rect.x < 1250:
			if self.rect.y >= 600 - self.rect.height:
				self.rect.y = 600 - self.rect.height
				self.square_y_speed = 0
				self.on_ground = True
		else:
			self.on_ground = False
		player_rect = self.rect
		
		for rect_pos_x, rect_pos_y, rect_width, rect_height in [(350, 600, 1500 - 650, 800), 
																(150, 375, 1500 - 1430, 800 - 750), 
																(700, 250, 1500 - 1240, 800 - 700), 
																(1175, 325, 1500 - 1275, 800 - 700)]:
			rect = py.Rect(rect_pos_x, rect_pos_y, rect_width, rect_height)
			if player_rect.colliderect(rect):
				# Xử lý va chạm ở đây
				# Ví dụ: khi va chạm, bạn có thể đặt vị trí của người chơi để không đi qua hình chữ nhật
				if self.square_y_speed > 0:  # Nếu đối tượng đang đi xuống
					self.rect.bottom = rect.top  # Đặt vị trí dưới cùng của đối tượng bằng vị trí trên cùng của hình chữ nhật
					self.square_y_speed = 0
					self.on_ground = True
					  # Đặt vận tốc y về 0 để ngăn đối tượng tiếp tục đi xuống
				# elif self.square_y_speed < 0:  # Nếu đối tượng đang đi lên
				# 	self.rect.top = rect.bottom  # Đặt vị trí trên cùng của đối tượng bằng vị trí dưới cùng của hình chữ nhật
				# 	self.square_y_speed = 0  # Đặt vận tốc y về 0 để ngăn đối tượng tiếp tục đi lên

		


		# Giới hạn không cho khối vuông đi quá biên
		if self.rect.x < 0:
			self.rect.x = 0
		elif self.rect.x > 1500 - self.rect.width:
			self.rect.x = 1500 - self.rect.width

		# thực hiện đẩy player theo hướng đá 
		if self.state == 'PUS_R':
			self.rect.x += self.velocity_x
		else :
			self.rect.x -= self.velocity_x

		# Áp dụng ma sát
		if self.velocity_x > 0:
			self.velocity_x -= 0.2  # Giảm tốc độ dương
		elif self.velocity_x < 0:
			self.velocity_x += 0.2  # Giảm tốc độ âm
		if abs(self.velocity_x) < 0.2:
			self.velocity_x = 0  # Đảm bảo tốc độ không trở thành số âm nhỏ
			if self.state == 'PUS_R' or self.state == 'PUS_L':
				self.state = 'NO'
		
		# Kiểm tra không cho khối vuông đi ra ngoài màn hình bên trái
		if self.rect.left < 0:
			self.rect.left = 0
			self.velocity_x = 0  # Đặt tốc độ thành 0 nếu chạm cạnh bên trái của màn hình

		if self.move_left_key == None:
			return 
		
		if not self.moveEnable:
			return

		# kiểm tra input từ bàn phím
		if key[self.move_left_key]:
			self.go_left()
		elif key[self.move_right_key]:
			self.go_right()
		else:
			self.right = False
			self.left = False
		if key[self.jump_key] and self.click_jump_enable and self.Max_jump > 0:
			self.do_jump()

		if not self.click_jump_enable:
			self.key_twice -= 1
			if self.key_twice <= 0:
				self.click_jump_enable = True

		if self.on_ground: 
			self.Max_jump = 2
			self.key_twice = 10
			
		# else:
		# 	self.click_jump_enable = True
		# 	if self.on_ground: 
		# 		self.Max_jump = 2

		

	def __str__(self):   # Tạo một chuỗi đại diện cho đối tượng Player
		player_info = [
			str(self.speed), # 0
			str(self.Max_jump), # 1
			str(self.on_ground), # 2
			str(self.square_y_speed), # 3
			str(self.GRAVITY), # 4
			str(self.JUMP_POWER), # 5
			self.state, # 6
			str(self.max_health), # 7
			str(self.health), # 8 
			str(self.velocity_x), # 9
			str(self.rect.x), # 10
			str(self.rect.y), # 11
			str(self.side), # 12
			str(self.walkCount), # 13
			str(self.kicAcount), # 14
			str(self.atkAcount), # 15
			str(self.sp1count), # 16
			str(self.idlecount), # 17
			str(self.right), # 18
			str(self.left), # 19
			str(self.key_twice), # 20
			str(self.name) # 20
		]
		return ",".join(player_info)

	def from_string(self, player_str):  # chuyển string lấy từ server thành giá trị cho player
		values = player_str.split(",")
		self.speed = int(values[0])
		self.Max_jump = int(values[1])
		self.on_ground = values[2].lower() == 'true'
		self.square_y_speed = float(values[3])
		self.GRAVITY = float(values[4])
		self.JUMP_POWER = float(values[5])
		self.state = values[6]
		self.max_health = int(values[7])
		self.health = int(values[8])
		self.velocity_x = float(values[9])
		self.rect.x = float(values[10])
		self.rect.y = float(values[11])
		self.side = values[12]
		self.walkCount = int(values[13])
		self.kicAcount = int(values[14])
		self.atkAcount = int(values[15])
		self.sp1count = int(values[16])
		self.idlecount = int(values[17])
		self.right = values[18].lower() == 'true'
		self.left = values[19].lower() == 'true'
		self.key_twice = values[20].lower() == 'true'
		self.name = values[21]