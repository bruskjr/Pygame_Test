import pygame

import projectiles
from entity import Character


class Player(Character):
	def __init__(self, x, y, level, keyboard, mouse):
		super(Player, self).__init__(x, y, level)
		self.image = pygame.Surface((32,64))
		self.image.fill(pygame.Color("#FF0000"))
		self.rect = pygame.Rect(x, y, 32, 64)
		self.keyboard = keyboard
		self.mouse = mouse

		self.speed = 500
		self.fire_rate = 0

		# Keep track of player ammo
		self.bullets = pygame.sprite.Group()

	def update(self, dt):
		keysDown = self.keyboard.keysDown
		right = False
		left = False

		# Jumping
		if ((pygame.K_w in keysDown and keysDown[pygame.K_w]) 
			or (pygame.K_SPACE in keysDown and keysDown[pygame.K_SPACE])):
				if self.onGround:
					self.yvel = -600
		
		# Left Movement
		if pygame.K_a in keysDown and keysDown[pygame.K_a]:
			left = True
			self.xvel = -(self.speed)
		
		# Right movement
		if pygame.K_d in keysDown and keysDown[pygame.K_d]:
			right = True
			self.xvel = self.speed

		# Standing
		if not (right or left):
			self.xvel = 0

		# Check if left mouse is down
		if self.mouse.buttonsDown[0] and self.fire_rate == 0:
			self.fire_rate = 5
			self.fire()
		elif self.fire_rate > 0:
			self.fire_rate -= 1

		# Update player bullets
		for bullet in self.bullets:
			bullet.update(dt)

		super(Player, self).update(dt)
	
	def pos(self):
		''' Return player position '''
		return self.rect.center

	def fire(self):
		''' Fire currently selected ammo '''
		bullet = projectiles.Rocket(self)
		self.bullets.add(bullet)
  		bullet.fire(self.mouse.pos(), self.pos())
		