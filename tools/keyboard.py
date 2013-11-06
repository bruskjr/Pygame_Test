import pygame

class Keyboard:
	def __init__(self):
		self.keysDown = {}	

	def update(self):
		for e in pygame.event.get():
			if e.type == pygame.QUIT: 
				raise SystemExit, "QUIT"
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_ESCAPE:
					raise SystemExit, "ESCAPE"
				else:
					self.keysDown[e.key] = True
			if e.type == pygame.KEYUP:
				self.keysDown[e.key] = False