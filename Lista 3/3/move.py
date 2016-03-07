# -*- encoding: utf8 -*-
import sys
import pygame
import math
from pygame.locals import *

class Snowman(object):
	frames = 60
	def __init__(self, creen):
		self.screen = screen

	def draw(self, frame, x = 100, y = 150, side = 1, type = 1):
		frame = frame % self.frames
		# BACK HAND
		if type == 1:
			pygame.draw.line(self.screen, (75, 25, 0),
				(x, y - 75), (x + side * 35, y - 75 + 20 * math.sin(2 * math.pi / self.frames * (frame + 1))), 4)

		elif type == 2:
			pygame.draw.lines(self.screen, (75, 25, 0), False, (
				(x, y - 75), 
				(x - side * 15, y - 75 - 7 * math.sin(2 * math.pi / self.frames * (frame + 1))),
				(x - side * 30, y - 75 + 14 * math.sin(2 * math.pi / self.frames * (frame + 1))),
				(x - side * 35, y - 75 - 20 * math.sin(2 * math.pi / self.frames * (frame + 1))),
				), 4)

		# BODY
		bottom = int(28 + 2 * math.sin(2 * math.pi / self.frames * (frame + 1)))
		middle = int(18 + 2 * math.sin(2 * math.pi / self.frames * (frame + 1)))
		head = int(8 + 2 * math.sin(2 * math.pi / self.frames * (frame + 1)))
		pygame.draw.circle(self.screen, (255, 255, 255), (x, y - bottom), bottom)
		pygame.draw.circle(self.screen, (255, 255, 255), (x, y - 2 * bottom - middle + 5), middle)
		pygame.draw.circle(self.screen, (255, 255, 255), (x, y - 2 * (bottom + middle) - head + 10), head)

		#HAT
		pygame.draw.polygon(self.screen, type == 1 and (0, 125, 0) or (125, 0, 0) , (
			(x, y - 2 * (bottom + middle + head) - 10), (x - 3, y - 2 * (bottom + middle + head) - 10),
			(x - 3, y - 2 * (bottom + middle + head) + 5), (x - 16, y - 2 * (bottom + middle + head) + 5), 
			(x - 16, y - 2 * (bottom + middle + head) + 10), (x + 16, y - 2 * (bottom + middle + head) + 10),
			(x + 16, y - 2 * (bottom + middle + head) + 5), (x + 3, y - 2 * (bottom + middle + head) + 5),
			(x + 3, y - 2 * (bottom + middle + head) - 10),
		)) 

		# FRONT HAND
		if type == 1:
			pygame.draw.line(self.screen, (75, 25, 0),
				(x, y - 2 * bottom - middle), (x + side * 35, y - 75 - 20 * math.sin(2 * math.pi / self.frames * (frame + 1))), 4)

		elif type == 2:
			pygame.draw.lines(self.screen, (75, 25, 0), False, (
				(x, y - 2 * bottom - middle), 
				(x + side * 15, y - 75 + 7 * math.sin(2 * math.pi / self.frames * (frame + 1))),
				(x + side * 30, y - 75 - 14 * math.sin(2 * math.pi / self.frames * (frame + 1))),
				(x + side * 35, y - 75 + 20 * math.sin(2 * math.pi / self.frames * (frame + 1))),
				), 4)


		# NOSE
		pygame.draw.polygon(self.screen, (250, 160, 0), (
			(x + side * 9, y - 2 * (bottom + middle)), 
			(x + side * 9, y - 2 * (bottom + middle) + 4), 
			(x + side * 19, y - 2 * (bottom + middle) + 2),
		))

		#EYE
		pygame.draw.circle(self.screen, (0, 0, 0), (x + side * 8, y - 2 * (bottom + middle)), 2)


if __name__ == "__main__":
	pygame.init()
	clock = pygame.time.Clock()
	screen = pygame.display.set_mode((640, 480))
	pygame.display.set_caption("Animacja")
	snowman = Snowman(screen)
	background = pygame.image.load("background.jpg").convert()
	width = background.get_width()
	i = 0
	posx = 0
	posy = 480
	side = 1
	while True:
		clock.tick(80)
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit()
				
		pressed = pygame.key.get_pressed()
		delta = 2
		type = 1
		if True in (pressed[K_UP], pressed[K_LEFT], pressed[K_DOWN], pressed[K_RIGHT]):
			if pressed[K_LSHIFT] | pressed[K_RSHIFT]:
				type = 2
				delta = 3

			if pressed[K_UP]:
				posy -= delta

			elif pressed[K_DOWN]:
				posy += delta

			if pressed[K_LEFT]:
				posx += delta
				side = -1

			elif pressed[K_RIGHT]:
				posx -= delta
				side = 1
    
		if posx > width:
			posx -= width

		if posx < 0:
			posx += width

		if posy < 400:
			posy = 400

		if posy > 480:
			posy = 480

		screen.blit(background, (posx,0))
		screen.blit(background, (posx - width,0))
		snowman.draw(i, 300, posy, side, type)
		i += 1
		pygame.display.update()
