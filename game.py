import pygame

from math import sqrt

W_WIDTH = 800 
W_HEIGHT = 600
H_WIDTH = W_WIDTH/2
H_HEIGHT = W_HEIGHT/2
DISPLAY = (W_WIDTH, W_HEIGHT)
DISPLAY = (W_WIDTH, W_HEIGHT)

# Setup and main game loop
def main():
	pygame.init()
	screen = pygame.display.set_mode(DISPLAY)
	pygame.display.set_caption("Game")

	game = Game(screen)
	game.setup(level1)
	game.run()
	


class Game():
	""" Game data """
	def __init__(self, screen):
		self.running = True
		self.screen = screen
		self.entities = pygame.sprite.Group()
		self.timer = pygame.time.Clock()
		self.level = level1
		self.camera = Camera(len(self.level.raw[0])*32, len(self.level.raw)*32)
		self.mouse = Mouse('images/crosshair.png', self.camera)
		self.keyboard = Keyboard()
		self.player = Player(32, 32, self.level, self.keyboard, self.mouse)
		self.enemies = [Goon(900,100, self.level), Goon(900,510, self.level), Goon(600,574, self.level)]
		self.debug = True
		self.font = pygame.font.SysFont("arial",12)

	def setup(self, map):
		""" Setup the current level """
		
		for p in self.level.platforms:
			self.entities.add(p)

		for e in self.enemies:
			self.entities.add(e)

		# Draw Player
		self.entities.add(self.player)

		# Hide system mouse cursor
		#self.mouse.hide_default_cursor()

	# Update the objects
	def update(self):
		self.timer.tick()
		self.camera.update(self.player)
		self.mouse.update()
		self.keyboard.update()
		self.player.update()

		for e in self.enemies:
			e.update()

	def draw(self):
		self.screen.fill((0, 0, 0))
		
		for e in self.entities:
			self.screen.blit(e.image, self.camera.apply(e))

		for b in self.player.bullets:
			self.screen.blit(b.image, self.camera.apply(b))

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

		#self.screen.blit(self.mouse.cursor, self.mouse.pos())

	def run(self):
		while self.running:
			self.timer.tick(60)

		 	self.update()
		 	self.draw()
		 	
		 	pygame.display.flip()


class Entity(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image =  pygame.Surface([32, 32])

	def update():
		pass

class Platform(Entity):
	def __init__(self, x, y):
		super(Platform, self).__init__()
		self.rect = pygame.Rect(x, y, 32, 32)

		self.image = pygame.Surface((32,32))
		self.image.fill(pygame.Color("#FFFFFF"))

	def update(self):
		pass

class Projectile(Entity):
	def __init__(self):
		super(Projectile, self).__init__()

		self.image =  pygame.Surface([5, 5])
		self.image.fill((255,255,255))

		self.rect = pygame.Rect(0,0,1,1)

		self.speed = 30

		self.xvel = 0
		self.yvel = 0

	def update(self):
		self.rect.x += self.xvel
		self.rect.y += self.yvel

	def calculate_velocity(self, start, end):
		v = (end[0]-start[0], end[1]-start[1])
		dist = sqrt(v[0]*v[0] + v[1]*v[1])
		return (v[0]*(1.0/dist)*self.speed, v[1]*(1.0/dist)*30)
		

	def fire(self, mouse_pos, player_pos):
		v = self.calculate_velocity(player_pos, mouse_pos)
		print v
		self.rect.x = player_pos[0]
		self.rect.y = player_pos[1]
		self.xvel = v[0]
		self.yvel = v[1]
		

class Moveable(Entity):
	def __init__(self, x, y, level):
		super(Moveable, self).__init__()
		self.xvel = 0
		self.yvel = 0
		self.onGround = False
		self.rect = pygame.Rect(x, y, 32, 32)
		self.level = level
	
	def update(self):

		""" Apply gravity to all moveable objects """
		if not self.onGround:
			self.yvel += 0.3
			if self.yvel > 30: self.yvel = 30

		self.rect.left += self.xvel
		self.collide(self.xvel, 0)
		self.rect.top += self.yvel
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

class Player(Character):
	def __init__(self, x, y, level, keyboard, mouse):
		super(Player, self).__init__(x, y, level)
		self.image = pygame.Surface((32,32))
		self.image.fill(pygame.Color("#FF0000"))
		self.keyboard = keyboard
		self.mouse = mouse
		self.bullets = pygame.sprite.Group()

	def update(self):
		keysDown = self.keyboard.keysDown
		right = False
		left = False
		if ((pygame.K_w in keysDown and keysDown[pygame.K_w]) 
			or (pygame.K_SPACE in keysDown and keysDown[pygame.K_SPACE])):
				if self.onGround:
					self.yvel -= 7
		
		if pygame.K_a in keysDown and keysDown[pygame.K_a]:
			left = True
			self.xvel = -5
		
		if pygame.K_d in keysDown and keysDown[pygame.K_d]:
			right = True
			self.xvel = 5

		if not (right or left):
			self.xvel = 0

		

		# Check if left mouse is down
		if self.mouse.buttonsDown[0]:
			self.fire()

		for bullet in self.bullets:
			bullet.update()

		super(Player, self).update()

	def pos(self):
		return self.rect.center

	def fire(self):
		bullet = Projectile()
  		bullet.fire(self.mouse.pos(), self.pos())
		self.bullets.add(bullet)


class Enemy(Character):
	def __init__(self, x, y, level):
		super(Enemy, self).__init__(x, y, level)

class Goon(Enemy):
	def __init__(self, x, y, level):
		super(Goon, self).__init__(x,y, level)
		self.image = pygame.Surface((32,32))
		self.image.fill(pygame.Color("#0000FF"))
		self.speed = 1
		self.xvel = self.speed

	def update(self):
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

		super(Goon, self).update()

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

class Level:
	""" Represents a game map """
	def __init__(self, level):
		self.raw = level
		self.platforms = []

		x = y = 0
		for row in level:
			for col in row:
				if col == "1":
					p = Platform(x, y)
					self.platforms.append(p)
				x += 32
			y += 32
			x = 0


class Mouse:
	def __init__(self, img_path, camera):
		self.buttonsDown = (False, False, False)
		self.cursor = pygame.image.load(img_path).convert_alpha()
		self.camera = camera

	def hide_default_cursor(self):
		pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

	def pos(self):
		c = self.camera.focus.topleft
		m = pygame.mouse.get_pos()
		return (m[0]-c[0], m[1]-c[1])

	def update(self):
		self.buttonsDown = pygame.mouse.get_pressed()


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
	"1                111111                1",
	"1                                      1",
	"11111111111111111111111111111111111111111" ])




if __name__ == "__main__":
	main()