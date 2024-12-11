import pygame as py

ATTACK_COOLDOWN = 500  # Thời gian hồi của đòn đánh (milliseconds)
STUNNED_COOLDOWN = 450 
PUSH_COOLDOWN = 600 
DAMAGE = 10
TEXT_COLOR = (255, 255, 255)

def check_collision(p1, p2):
	if p1.side == 'L':
		return py.Rect(p1.rect.x + p1.hitbox,p1.rect.y, 100,100).colliderect(p2.rect)
	else:
		return py.Rect(p1.rect.x - p1.hitbox,p1.rect.y, 100,100).colliderect(p2.rect)


def handle_attack(attacker, victim, newdame=None):
	if attacker == None or check_collision(attacker, victim) :
		if (newdame==None):
			victim.health -= DAMAGE
		else:
			victim.health -= newdame
		return True
	return False

def draw_atk_effect(screen, player):
	if player.state == 'ATK' or player.state == 'KIC':
		if player.side == 'L':
			py.draw.rect(screen, (255, 150, 0), py.Rect(player.rect.x, player.rect.y, player.SQUARE_SIZE_X, player.SQUARE_SIZE_Y))
		else:
			py.draw.rect(screen, (0, 150, 255), py.Rect(player.rect.x - 100, player.rect.y, player.SQUARE_SIZE_X, player.SQUARE_SIZE_Y))

def draw_attack_cooldown(screen, time_remaining, toado):
	font = py.font.SysFont(None, 24)
	text = font.render(f'Attack: {time_remaining / 1000:.1f} s', True, TEXT_COLOR)
	screen.blit(text, toado)

def draw_attack_ready(screen, toado):
	font = py.font.SysFont(None, 24)
	text = font.render('Attack: Ready', True, TEXT_COLOR)
	screen.blit(text, toado)

def draw_stunned_cooldown(screen, time_remaining, toado):
	font = py.font.SysFont(None, 24)
	text = font.render(f'Stunned: {time_remaining / 1000:.1f} s', True, TEXT_COLOR)
	screen.blit(text, toado)

def draw_stunned_ready(screen, toado):
	font = py.font.SysFont(None, 24)
	text = font.render('Stunned: No', True, TEXT_COLOR)
	screen.blit(text, toado)


def draw_push_cooldown(screen, time_remaining, toado):
	font = py.font.SysFont(None, 24)
	text = font.render(f'Pushed: {time_remaining / 1000:.1f} s', True, TEXT_COLOR)
	screen.blit(text, toado)

def draw_push_ready(screen, toado):
	font = py.font.SysFont(None, 24)
	text = font.render('Pushed: No', True, TEXT_COLOR)
	screen.blit(text, toado)

