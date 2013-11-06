import pygame

class Mouse:
	def __init__(self, camera):
		self.buttonsDown = (False, False, False)
		self.camera = camera

	def hide_cursor(self):
		pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

	# Return position of mouse relative to camera
	def pos(self):
		c = self.camera.focus.topleft
		m = pygame.mouse.get_pos()
		return (m[0]-c[0], m[1]-c[1])

	# Return the absolute position of the mouse
	def abs_pos(self):
		return pygame.mouse.get_pos()


	def update(self):
		self.buttonsDown = pygame.mouse.get_pressed()
