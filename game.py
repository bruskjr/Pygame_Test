import pygame

W_WIDTH = 800 
W_HEIGHT = 600
H_WIDTH = W_WIDTH/2
H_HEIGHT = W_HEIGHT/2

DISPLAY = (W_WIDTH, W_HEIGHT)

# Setup and main game loop
def main():
	pygame.init()
	screen = pygame.display.set_mode(DISPLAY)
	pygame.display.set_caption("Game")

	game = Game()
	game.setup(level1)
	while game.running:
		game.timer.tick(60)

	 	update(game)
	 	draw(screen, game)
	 	
	 	pygame.display.flip()

# Update the objects
def update(game):
	game.timer.tick()
	game.camera.update(game.player)
	game.keyboard.update()
	game.player.update()

	for e in game.enemies:
		e.update()

def draw(screen, game):
	screen.fill((0, 0, 0))
	
	for e in game.entities:
		screen.blit(e.image, game.camera.apply(e))

	if game.debug:
		s = pygame.Surface((200,50))	
		s.fill((0,0,255))
		screen.blit(s, (0,0))

		player_pos = game.font.render("Player: " + str(game.player.rect.bottomright), True,(255,255,255))
		fps = game.font.render("FPS: " + str(game.timer.get_fps()), True,(255,255,255))
		screen.blit(player_pos,(5,0))
		screen.blit(fps,(5,12))


class Game():
	""" Game data """
	def __init__(self):
		self.running = True
		self.entities = pygame.sprite.Group()
		self.timer = pygame.time.Clock()
		self.level = level1
		self.keyboard = Keyboard()
		self.camera = Camera(len(self.level.raw[0])*32, len(self.level.raw)*32)
		self.player = Player(32, 32, self.level, self.keyboard)
		self.enemies = [Goon(900,100, self.level), Goon(900,510, self.level), Goon(600,574, self.level)]
		self.debug = True
		self.font = pygame.font.SysFont("arial",12)

	def setup(self, map):
		""" Setup the current level """
		
		for p in self.level.platforms:
			self.entities.add(p)

		for e in self.enemies:
			self.entities.add(e)


		self.entities.add(self.player)

class Entity(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((32,32))
		self.image.convert

	def update():
		pass

class Platform(Entity):
	def __init__(self, x, y):
		super(Platform, self).__init__()
		self.rect = pygame.Rect(x, y, 32, 32)
		self.image.fill(pygame.Color("#FFFFFF"))

	def update(self):
		pass

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
	def __init__(self, x, y, level, keyboard):
		super(Player, self).__init__(x, y, level)
		self.image.fill(pygame.Color("#FF0000"))
		self.keyboard = keyboard

	def update(self):
		keysDown = self.keyboard.keysDown
		right = False
		left = False
		if pygame.K_UP in keysDown and keysDown[pygame.K_UP]:
			if self.onGround:
				self.yvel -= 7
		
		if pygame.K_LEFT in keysDown and keysDown[pygame.K_LEFT]:
			left = True
			self.xvel = -5
		

		if pygame.K_RIGHT in keysDown and keysDown[pygame.K_RIGHT]:
			print keysDown
			right = True
			self.xvel = 5

		if not (right or left):
			self.xvel = 0

		super(Player, self).update()

class Enemy(Character):
	def __init__(self, x, y, level):
		super(Enemy, self).__init__(x, y, level)

class Goon(Enemy):
	def __init__(self, x, y, level):
		super(Goon, self).__init__(x,y, level)
		self.image.fill(pygame.Color("#0000FF"))
		self.speed = 2
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
				self.xvel = -(self.xvel) 

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

class Camera:
	def __init__(self, width, height):
		self.focus = pygame.Rect(0,0,width,height)
		self.width = width
		self.height = height

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