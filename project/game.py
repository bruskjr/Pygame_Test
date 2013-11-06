import pygame

from entity import *
from enemies.goon import Goon
from player import Player
from levels.level import *
from constants import *
import tools

class Game():
	""" Game data """
	def __init__(self):
		self.screen = pygame.display.set_mode(DISPLAY)
		pygame.display.set_caption("Game")
		
		self.running = True
		self.debug = True

		# Load game clock
		self.timer = pygame.time.Clock()

		# Load starting level
		self.level = level1

		# Game tools
		self.camera = tools.Camera(len(self.level.raw[0])*32, len(self.level.raw)*32)
		self.mouse = tools.Mouse(self.camera)
		self.keyboard = tools.keyboard.Keyboard()
		self.crosshair = tools.Crosshair('assets/images/crosshair.png', self.mouse)

		# Add Game objects
		self.entities = pygame.sprite.Group()
		self.player = Player(32, 32, self.level, self.keyboard, self.mouse) 
		
		self.font = pygame.font.SysFont("arial",12)
		self.setup(level1)

	def setup(self, map):
		""" Setup the current level """
		
		for p in self.level.platforms:
			self.entities.add(p)

		for e in self.level.enemies:
			self.entities.add(e)

		# Draw Player
		self.entities.add(self.player)

	# Update the objects
	def update(self):
		# Calculate delta time
		dt = self.timer.tick(60)
		dt /= 1000.0
		
		# Update tools
		self.camera.update(self.player)
		self.mouse.update()
		self.keyboard.update()
		self.crosshair.update()

		# Update player
		self.player.update(dt)

		# Update enemies
		for e in self.level.enemies:
			e.update(dt)

	def draw(self):
		self.screen.fill((0, 0, 0))
		
		for e in self.entities:
			e.draw(self.screen, self.camera.apply(e))

		for b in self.player.bullets:
			b.draw(self.screen, self.camera.apply(b))

			
		if self.debug:
			s = pygame.Surface((200,50))	
			s.fill((0,0,255))
			self.screen.blit(s, (0,0))

			player_pos = self.font.render("Player: " + str(self.player.pos()), True,(255,255,255))
			mouse_pos = self.font.render("Mouse: " + str(self.mouse.pos()), True,(255,255,255))
			camera_pos = self.font.render("Camera: " + str(self.camera.focus.topleft), True,(255,255,255))
			fps = self.font.render("FPS: " + str(self.timer.get_fps()), True,(255,255,255))
			self.screen.blit(player_pos,(5,0))
			self.screen.blit(mouse_pos,(5,12))
			self.screen.blit(camera_pos,(5,24))
			self.screen.blit(fps,(5,36))

		# Draw reticle
		self.crosshair.draw(self.screen)
		

	def run(self):
		while self.running:
			self.timer.tick(60)

		 	self.update()
		 	self.draw()
		 	
		 	pygame.display.flip()








