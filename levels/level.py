import pygame
from project.platform import Platform
from project.enemies.goon import Goon

class Level:
	""" Represents a game map """
	def __init__(self, level):
		self.raw = level
		self.platforms = pygame.sprite.Group()
		self.enemies = pygame.sprite.Group()

		enemies = [Goon(900,100, self), Goon(900,510, self), Goon(600,574, self)]
		for enemy in enemies:
			self.enemies.add(enemy)

		x = y = 0
		for row in level:
			for col in row:
				if col == "1":
					p = Platform(x, y)
					self.platforms.add(p)
				x += 32
			y += 32
			x = 0

level1 = Level([
	"1111111111111111111111111111111111111111",
	"1                                      1",
	"1                                      1",
	"1                                      1",
	"1                                      1",
	"11111111111111111                      1",
	"1                                      1",
	"1                       1111111111111111",
	"1                                      1",
	"1                                      1",
	"1                                      1",
	"1                                      1",
	"1                                      1",
	"1                                      1",
	"1         111111                       1",
	"1                                      1",
	"1                        111111        1",
	"1                                      1",
	"1               11 111111              1",
	"1                                      1",
	"11111111111111111111111111111111111111111" ])