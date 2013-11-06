import pygame
from project.constants import *

class Camera:
	def __init__(self, width, height):
		self.focus = pygame.Rect(0,0,width,height)
		self.width = width
		self.height = height

	def offset(self, pos):
		v = self.focus.topleft
		return (pos[0]-v[0], pos[1]-v[0])

	def apply(self, entity):
		return entity.rect.move(self.focus.topleft)
 
	def update(self, entity):
		l, t, _, _ = entity.rect
		_, _, w, h = self.focus
		l, t, _, _ = -l+H_WIDTH, -t+H_HEIGHT, w, h

		l = min(0,l)
		l = max(-(self.width-W_WIDTH), l)
		t = max(-(self.height-W_HEIGHT), t)
		t = min(0, t)
		self.focus = pygame.Rect(l, t, w, h)