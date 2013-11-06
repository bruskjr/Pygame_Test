import pygame
import math 

from tools.vectors import Vector2
from constants import *
from entity import Entity

class Projectile(Entity):
	def __init__(self, player=None):
		super(Projectile, self).__init__()

		self.player = player
		self.image =  pygame.Surface([3, 3])
		self.image.fill((0,255,0))

		self.rect = pygame.Rect(0,0,3,3)

		self.speed = 2000
		self.direction = Vector2(0.0,0.0)

		# Track position rounding
		self.pos_correct = Vector2(0, 0)

		# Amount of damage the ammo does
		self.damage = 0

	def update(self, dt):

		dx = self.direction.x * self.speed * dt
		dy = self.direction.y * self.speed *  dt

		self.adjust_trajectory(dx,dy)

		self.rect.x += dx
		self.rect.y += dy

		self.collide()
		
	def collide(self):
		# Enemy Collisions
		player = self.player
		enemy_col = pygame.sprite.spritecollide(self, player.level.enemies, False, pygame.sprite.collide_circle)
		for enemy in enemy_col:
			self.kill()
			enemy.health -= self.damage

		# Platform collisions
		platform_col = pygame.sprite.spritecollide(self, player.level.platforms, False)
		for platform in platform_col:
			self.kill()


	# Adjust trajectory for rect rounding errors
	def adjust_trajectory(self, dx, dy):
		self.pos_correct += Vector2(dx - math.floor(dx), dy - math.floor(dy))
		
		if self.pos_correct.x > 1:
			self.rect.x += 1
			self.pos_correct.x = 0

		if self.pos_correct.y > 1:
			self.rect.y += 1
			self.pos_correct.y = 0

	def rotate(self, angle):
		''' Rotate projectile to the desired angle '''
		self.image = pygame.transform.rotozoom(self.image, angle, 1.0)


	def fire(self, mouse_pos, player_pos):
		self.direction = (Vector2(mouse_pos) - Vector2(player_pos)).normalize()

		# Set starting position
		self.rect.x = player_pos[0]
		self.rect.y = player_pos[1]
		

class Bullet(Projectile):
	def __init__(self, player):
		super(Bullet, self).__init__(player)
		self.damage = 1

class Rocket(Projectile):
	def __init__(self, player):
		super(Rocket, self).__init__(player)
		self.damage = 1
		self.speed = 1000
		self.radius = 5