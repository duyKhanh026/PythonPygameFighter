import pygame as py
from classes.player import Player

class Character2(Player): # the blue guy 
	def __init__(self, strNam, x, y, color, move_left_key, move_right_key, jump_key, atk_key, def_key, kick_key, sp1_key, side):
		super().__init__(strNam, x, y, color, move_left_key, move_right_key, jump_key, atk_key, def_key, kick_key, sp1_key, side)
		
		self.charIdle_sp = [py.image.load(f'assets/purple_sp/stickman_idle{i}.png') for i in range(1, 6)]
		self.walkRight_sp = [py.image.load(f'assets/purple_sp/stickman_running{i}.png') for i in range(1, 6)]
		self.slashA1_sp = [py.image.load(f'assets/purple_sp/stickman_punch{i}.png') for i in range(1, 5)]
		self.speed = 6

	def skill_active(self, screen, player2):
		return False

	def redrawGameWindow(self, surface):
		if self.walkCount + 1 >= 30: # 5frame
			self.walkCount = 0
		if self.kicAcount + 1 >= 42: # 7frame
			self.kicAcount = 0
		if self.sp1count + 1 >= 300: # 19 frame
			self.skill1 = False
			self.max_health = 100
			self.health = self.health / 2
			self.dame = 10
			self.hitbox = 100
			self.sp1count = 0
			self.block_def = False
			self.block_kick = False
		elif self.skill1:
			self.sp1count += 1 
		if self.idlecount >= 30:
			self.idlecount = 0

		if self.state == 'SP1' and self.max_health == 100:
			self.skill1 = True
			self.max_health = 200
			self.hitbox = 150
			self.health = self.health + 100
			self.dame = 20
			self.state = 'NO'
			self.block_def = True
			self.block_kick = True

		if self.skill1:
			if self.state == 'ATK':
				if self.atkAcount < 23:
					self.atkAcount += 1
				elif self.atkAcount > 23:
					self.atkAcount = 0
				surface.blit(self.slashA1_sp[self.atkAcount//6] if self.side == 'L' else py.transform.flip(self.slashA1_sp[self.atkAcount//6], True, False), (self.rect.x - 200, self.rect.y - 200))
			elif self.state == 'KIC':
				surface.blit(self.kickA[self.kicAcount//6] if self.side == 'L' else py.transform.flip(self.kickA[self.kicAcount//6], True, False), (self.rect.x - self.rect.width, self.rect.y))
				self.kicAcount += 1
			elif self.right:
				surface.blit(self.walkRight_sp[self.walkCount//6], (self.rect.x - self.rect.width, self.rect.y - 100))
				self.walkCount += 1
			elif self.left:
				surface.blit(py.transform.flip(self.walkRight_sp[self.walkCount//6], True, False), (self.rect.x - self.rect.width, self.rect.y - 100))
				self.walkCount += 1
			elif self.state == 'DEF':
				surface.blit(self.defenseA if self.side == 'L' else py.transform.flip(self.defenseA, True, False), (self.rect.x - self.rect.width, self.rect.y))
			else :
				surface.blit(self.charIdle_sp[self.idlecount//6] if self.side == 'L' else py.transform.flip(self.charIdle_sp[self.idlecount//6], True, False), (self.rect.x - self.rect.width, self.rect.y - self.rect.height + 50))
				self.idlecount += 1

		else : 
			return super().redrawGameWindow(surface)
		