import os, pygame, random, sys
from pygame.locals import *

"""positions and sizes"""
origin = 0, 0
screen_size = width, height = 640, 480
ship_size = 36, 52
ship_sprite_pos = 4, 8
ship_pos = width / 2, height - 64
bullet_size = 18, 40
bullet_pos = 96, 480
enemy_sprite_pos = 338, 84
enemy_size = 36, 48
scorebox_pos = width * 7 / 10, 0
lose_pos = width * 3 / 20, height * 2 / 5

"""colors and speeds"""
white = 250, 250, 250
black = 0, 0, 0
ship_speed = 3.5
dumb_speed = 1.5
bullet_speed = 12
scroll_speed = 1.5

"""filenames"""
spritesheet = 'spritesheet.png'
sky = 'road.png'

class Bullet(pygame.sprite.Sprite):
	"""defines a bullet, which is shot by ships"""
	def __init__(self, image, speed, pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = pos
		self.speed = speed

	def move(self):
		self.rect = self.rect.move(0, -self.speed)

	def draw(self, screen):
		screen.blit(self.image, (self.rect.topleft))

class Ship(pygame.sprite.Sprite):
	"""defines a ship, the generic unit in the game"""
	def __init__(self, image, speed, pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.speed = speed
		self.rect = self.image.get_rect()
		self.rect.topleft = pos
		self.v_x, self.v_y = 0, 0

	def hit(self, rect):
		if self.rect.colliderect(rect):
			return True

	def move(self, screen):
		self.rect = self.rect.move(self.speed * self.v_x, self.speed * self.v_y)

	def draw(self, screen):
		screen.blit(self.image, (self.rect.topleft))

class DumbEnemy(Ship):
	"""defines an enemy grunt, which does not shoot"""
	def __init__(self, image, speed, pos):
		Ship.__init__(self, image, speed, pos)
		self.v_y = 1

class Player(Ship):
	"""defines a player, who can move and shoot"""
	def __init__(self, ship_img, bullet_img, pos):
		Ship.__init__(self, ship_img, ship_speed, pos)
		self.bullet_speed = bullet_speed
		self.bullet_img = bullet_img

	def update(self, v_x, v_y, screen):
		self.v_x, self.v_y = v_x, v_y
		rect = self.rect.move(self.speed * self.v_x, self.speed * self.v_y)
		if screen.get_rect().contains(rect):
			self.rect = rect

	def shoot(self, bullets):
		b = Bullet(self.bullet_img, self.bullet_speed, 
			(self.rect.left + self.rect.width / 4, 
				self.rect.top - self.rect.height / 2))
		bullets.append(b)

class Road(pygame.sprite.Sprite):
	"""defines a scrolling background"""
	def __init__(self, image, screen, speed):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.copy = image, image
		self.speed = speed
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

def handle_input(player, screen, bullets):
	"""handles keyboard input and window close events"""
	x, y = player.v_x, player.v_y
	for event in pygame.event.get():
		if event.type == QUIT:
			sys.exit()
		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				sys.exit()
			if event.key == K_SPACE:
				player.shoot(bullets)
			if event.key == K_UP:
				y -= 1
			if event.key == K_RIGHT:
				x += 1
			if event.key == K_DOWN:
				y += 1
			if event.key == K_LEFT:
				x -= 1
		elif event.type == KEYUP:
			if event.key == K_SPACE:
				player.shooting = 0
			if event.key == K_UP:
				y += 1
			if event.key == K_RIGHT:
				x -= 1
			if event.key == K_DOWN:
				y -= 1
			if event.key == K_LEFT:
				x += 1
	player.update(x, y, screen)

def initial_load(screen):
	"""creates road and player objects"""
	road_img = get_sprite(sky, origin, None)
	ship_img = get_sprite(spritesheet, ship_sprite_pos, ship_size)
	bullet_img = get_sprite(spritesheet, bullet_pos, bullet_size)

	road = Road(road_img, screen, scroll_speed)
	player = Player(ship_img, bullet_img, ship_pos)
	return road, player

def main():
	"""initialize and load assets"""
	pygame.init()
	font = pygame.font.Font(None, 48)
	score = 0
	scorebox = font.render(str(score), True, white, black)
	lose = 'GAME OVER, ESC TO EXIT'
	gameover = False
	screen = pygame.display.set_mode(screen_size)
	bground = pygame.Surface(screen.get_size())
	bground.convert()
	bground.fill(black)

	road, player = initial_load(screen)
	enemy_img = get_sprite(spritesheet, enemy_sprite_pos, enemy_size)
	enemies = []
	bullets = []

	screen.blit(bground, origin)
	pygame.display.flip()

	while 1:
		"""updates"""
		if not gameover:
			if pygame.time.get_ticks() % 200 == 0:
				pos = (random.randint(1, width - enemy_size[0]), 0)
				if enemies:
					for e in enemies:
						if not e.rect.collidepoint(pos):
							enemy = DumbEnemy(enemy_img, dumb_speed, pos)
							enemies.append(enemy)
				else:
					enemy = DumbEnemy(enemy_img, dumb_speed, pos)
					enemies.append(enemy)

			for b in bullets:
				b.move()

			for e in enemies:
				killed = False
				for b in bullets:
					if e.hit(b.rect):
						killed = True
						bullets.remove(b)
						enemies.remove(e)
						score += 10
						break
				if player.hit(e.rect):
					gameover = True
				e.move(screen)
			handle_input(player, screen, bullets)
			road.update()

		"""draws"""
		screen.blit(bground, (origin))
		road.draw(screen)
		player.draw(screen)

		for e in enemies:
			e.draw(screen)
		for b in bullets:
			if screen.get_rect().contains(b):
				b.draw(screen)
			else:
				bullets.remove(b)
		scorebox = font.render('score: ' + str(score), True, white, black)
		screen.blit(scorebox, scorebox_pos)

		if gameover:
			losescreen = font.render(str(lose), True, white, black)
			screen.blit(losescreen, lose_pos)
			for event in pygame.event.get():
				if event.type == KEYDOWN and event.key == K_ESCAPE:
					sys.exit()

		pygame.display.flip()

if __name__ == '__main__': main()

