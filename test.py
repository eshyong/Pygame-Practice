import os, pygame, sys
from pygame.locals import *

origin = 0, 0
screen_size = width, height = 640, 480

class Car(pygame.sprite.Sprite):
	"""defines a car, the generic unit in the game"""
	def __init__(self, car_img, bullet_img):
		pygame.sprite.Sprite.__init__(self)
		self.bullets = []
		self.bullet_speed = 2
		self.speed = 5
		self.v_x, self.v_y = 0, 0
		self.car_img = car_img
		self.bullet_img = bullet_img
		self.rect = self.car_img.get_rect()
		self.x = self.rect.left
		self.y = self.rect.top

	def move(self):
		self.rect = self.rect.move(self.speed * self.v_x, self.speed * self.v_y)

	def shoot():
		self.bullets.append(self.y)

	def update(self, v_x, v_y):
		self.v_x = v_x
		self.v_y = v_y


	def draw(self, screen):
		screen.blit(self.car_img, (self.rect.topleft))
		if self.bullets is not None:
			for b in self.bullets:
				screen.blit(self.bullet_img, (b))

class Road(pygame.sprite.Sprite):
	"""defines a scrolling background"""
	def __init__(self, image, screen):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.copy = image, image
		self.speed = 3
		self.rect = self.image.get_rect()
		self.area = screen.get_rect()

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
	sheet = pygame.image.load(os.path.join('Data', file)).convert()
	if size is None:
		size = sheet.get_size()
	sheet.set_clip(pygame.Rect(pos, size))
	return sheet.subsurface(sheet.get_clip())

def get_input(player):
	x, y = player.v_x, player.v_y
	for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					sys.exit()
				if event.key == K_SPACE:
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
	return x, y

def main():
	pygame.init()
	screen = pygame.display.set_mode(screen_size)

	white = 250, 250, 250
	black = 0, 0, 0

	sprite_size = 48, 64
	bullet_size = 28, 48
	bullet_pos = 90, 480

	road_img = get_sprite('road.jpeg', origin, None)
	road = Road(road_img, screen)
	car_img = get_sprite('spritesheet.png', origin, sprite_size)
	bullet_img = get_sprite('spritesheet.png', bullet_pos, bullet_size)
	player = Car(car_img, bullet_img)

	bground = pygame.Surface(screen.get_size())
	bground.convert()
	bground.fill(black)

	screen.blit(bground, (origin))
	pygame.display.flip()

	font = pygame.font.Font(None, 36)

	while 1:
		player.v_x, player.v_y = get_input(player)
		player.update(x, y)
		road.update()
		player.move()
		screen.blit(bground, (origin))
		road.draw(screen)
		player.draw(screen)
		pygame.display.flip()

if __name__ == '__main__': main()