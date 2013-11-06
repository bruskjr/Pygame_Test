import pygame
from project.entity import Enemy

class Goon(Enemy):
	def __init__(self, x, y, level):
		super(Goon, self).__init__(x,y, level)
		self.image = pygame.Surface((32,32))
		self.image.fill(pygame.Color("#0000FF"))
		self.speed = 200
		self.xvel = self.speed

		# Character stats
		self.health = 1

	def update(self, dt):
		# Edge detection
		if self.xvel != 0:
			e = self.rect.bottomright
			point = (1,1)
			if self.xvel < 0:
				e = self.rect.bottomleft
				point = (-1,1)
			cp = map(sum, zip(e, point))

			collide = False
			for p in self.level.platforms:
				if p.rect.collidepoint(cp):
					collide = True

			if not collide:		
				self.xvel *= -1

		super(Goon, self).update(dt)

	def collide(self, xvel, yvel):
		for p in self.level.platforms:
			if pygame.sprite.collide_rect(self, p):
				if xvel > 0: 
					self.rect.right = p.rect.left
					self.xvel = -(self.speed)
				if xvel < 0: 
					self.rect.left = p.rect.right
					self.xvel = self.speed
				if yvel > 0:
					self.rect.bottom = p.rect.top
					self.onGround = True
					self.yvel = 0
				if yvel < 0: 
					self.rect.top = p.rect.bottom