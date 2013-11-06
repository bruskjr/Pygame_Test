import pygame

from math import sqrt

class Entity(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image =  pygame.Surface([32, 32])
		self.rect = None

	def update(self):
		pass

	def draw(self, screen, pos):
		screen.blit(self.image, pos)


class Moveable(Entity):
	def __init__(self, x, y, level):
		super(Moveable, self).__init__()
		self.xvel = 0
		self.yvel = 0
		self.onGround = False
		self.rect = pygame.Rect(x, y, 32, 32)
		self.level = level
	
	def update(self, dt):
		""" Apply gravity to all moveable objects """
		if not self.onGround:
			self.yvel += 40
			if self.yvel > 800: self.yvel = 800

		self.rect.left += self.xvel * dt
		self.collide(self.xvel, 0)
		self.rect.top += self.yvel * dt
		self.onGround = False;
		self.collide(0, self.yvel)

		

	def collide(self, xvel, yvel):
		for p in self.level.platforms:
			if pygame.sprite.collide_rect(self, p):
				if xvel > 0: 
					self.rect.right = p.rect.left
				if xvel < 0: 
					self.rect.left = p.rect.right
				if yvel > 0:
					self.rect.bottom = p.rect.top
					self.onGround = True
					self.yvel = 0
				if yvel < 0: 
					self.rect.top = p.rect.bottom

class Character(Moveable):
	def __init__(self, x, y, level):
		super(Character, self).__init__(x, y, level)
		self.health = 5

class Enemy(Character):
	def __init__(self, x, y, level):
		super(Enemy, self).__init__(x, y, level)

	def update(self, dt):

		if self.health <= 0:
			self.kill()

		super(Enemy, self).update(dt)