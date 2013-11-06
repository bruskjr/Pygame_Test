import pygame

class Crosshair:
	def __init__(self, img_path, mouse):
		self.x = 0
		self.y = 0
		self.mouse = mouse
		self.image = pygame.image.load(img_path).convert_alpha()
		self.rect = self.image.get_rect()
		self.offset_x = self.rect.width/2
		self.offset_y = self.rect.height/2
		self.mouse.hide_cursor()

	def update(self):
		pos = self.mouse.abs_pos()
		self.x = pos[0]
		self.y = pos[1]

	def pos(self):
		return (self.x-self.offset_x, self.y-self.offset_y)

	def draw(self, screen):
		screen.blit(self.image, self.pos())