import pygame
from entity import Entity

class Platform(Entity):
	def __init__(self, x, y):
		super(Platform, self).__init__()
		self.rect = pygame.Rect(x, y, 32, 32)

		self.image = pygame.Surface((32,32))
		self.image.fill(pygame.Color("#FFFFFF"))

	def update(self):
		pass
		