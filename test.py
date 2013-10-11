import os, pygame, sys
from pygame.locals import *

"""positions and sizes"""
origin = 0, 0
screen_size = width, height = 640, 480
ship_size = 46, 64
ship_pos = 0, 0
bullet_size = 23, 48
bullet_pos = 93, 480

"""colors and speeds"""
white = 250, 250, 250
black = 0, 0, 0
ship_speed = 5
bullet_speed = 8

class Bullet(pygame.sprite.Sprite):
	"""defines a bullet, which is shot by ships"""
	def __init__(self, image, speed):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.speed = speed

	def move(self):
		self.rect = self.rect.move(0, -self.speed)

	def draw(self, screen):
		screen.blit(self.image, (self.rect.topleft))

class Ship(pygame.sprite.Sprite):
	"""defines a ship, the generic unit in the game"""
	v_x, v_y = 0, 0
	def __init__(self, image, speed):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.speed = speed
		self.rect = self.image.get_rect()

	def move(self, screen):
		rect = self.rect.move(self.speed * self.v_x, self.speed * self.v_y)
		if screen.get_rect().contains(rect):
			self.rect = rect

	def draw(self, screen):
		screen.blit(self.image, (self.rect.topleft))

class DumbEnemy(Ship):
	"""defines a standard enemy"""
	def __init__(self, image, speed, pos):
		Ship.__init__(self, image, speed)
		self.rect.topleft = pos
		self.v_y = 1

	def move(self, screen):
		Ship.move(self, screen)

class Player(Ship):
	"""defines a player, which moves and shoots"""
	def __init__(self, ship_img, bullet_img):
		Ship.__init__(self, ship_img, ship_speed)
		self.bullets = []
		self.bullet_speed = bullet_speed
		self.bullet_img = bullet_img

	def update(self, v_x, v_y, screen):
		self.v_x, self.v_y = v_x, v_y
		Ship.move(self, screen)
		for b in self.bullets:
			b.move()

	def shoot(self):
		b = Bullet(self.bullet_img, self.bullet_speed)
		b.rect.top = self.rect.top
		b.rect.left = self.rect.left + self.rect.width / 4
		self.bullets.append(b)

	def draw(self, screen):
		Ship.draw(self, screen)
		for b in self.bullets:
			if screen.get_rect().contains(b):
				b.draw(screen)
			else:
				self.bullets.remove(b)

class Road(pygame.sprite.Sprite):
	"""defines a scrolling background"""
	def __init__(self, image, screen):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.copy = image, image
		self.speed = 3
		self.area = screen.get_rect()
		self.rect = self.image.get_rect()

	def scroll(self):
		self.rect = self.rect.move(0, self.speed)

	def update(self):
		if self.rect.top == self.area.height:
			self.rect.topleft = origin
		self.scroll()

	def draw(self, screen):
		screen.blit(self.image, (self.rect.topleft))
		screen.blit(self.copy, (self.rect.left, self.rect.top - self.rect.height))

def get_sprite(file, pos, size):
	"""locates and returns an image from a spritesheet"""
	sheet = pygame.image.load(os.path.join('Data', file)).convert()
	if size is None:
		size = sheet.get_size()
	sheet.set_clip(pygame.Rect(pos, size))
	return sheet.subsurface(sheet.get_clip())

def handle_input(player, screen):
	x, y = player.v_x, player.v_y
	for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					sys.exit()
				if event.key == K_SPACE:
					player.shoot()
				if event.key == K_UP:
					if y == 0:
						y = -1
					elif y == 1:
						y = 0
				if event.key == K_RIGHT:
					if x == 0:
						x = 1
					elif x == -1:
						x = 0
				if event.key == K_DOWN:
					if y == 0:
						y = 1
					elif y == -1:
						y = 0
				if event.key == K_LEFT:
					if x == 0:
						x = -1
					elif x == 1:
						x = 0
			elif event.type == KEYUP:
				if event.key == K_UP:
					if y == -1:
						y = 0
					elif y == 0:
						y = 1
				if event.key == K_RIGHT:
					if x == 1:
						x = 0
					elif x == 0:
						x = -1
				if event.key == K_DOWN:
					if y == 1:
						y = 0
					elif y == 0:
						y = 1
				if event.key == K_LEFT:
					if x == -1:
						x = 0
					elif x == 0:
						x = 1
	player.update(x, y, screen)

def main():
	pygame.init()
	screen = pygame.display.set_mode(screen_size)

	road_img = get_sprite('road.jpeg', origin, None)
	road = Road(road_img, screen)
	ship_img = get_sprite('spritesheet.png', ship_pos, ship_size)
	bullet_img = get_sprite('spritesheet.png', bullet_pos, bullet_size)
	player = Player(ship_img, bullet_img)

	bground = pygame.Surface(screen.get_size())
	bground.convert()
	bground.fill(black)

	screen.blit(bground, (origin))
	pygame.display.flip()

	font = pygame.font.Font(None, 36)

	while 1:
		handle_input(player, screen)
		road.update()
		screen.blit(bground, (origin))
		road.draw(screen)
		player.draw(screen)
		pygame.display.flip()

if __name__ == '__main__': main()