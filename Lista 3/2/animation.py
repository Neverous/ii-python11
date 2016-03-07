# -*- encoding: utf8 -*-
import sys
import pygame
import math
from pygame.locals import *

class Snowman(object):
	frames = 40
	def __init__(self, creen):
		self.screen = screen

	def draw(self, frame, x = 100, y = 150, side = 1, type = 1):
		frame = frame % self.frames
		# BODY
		# BACK HAND
		if type == 1:
			pygame.draw.line(self.screen, (75, 25, 0),
				(x/2, y - 75), (x/2 + side * 35, y - 75 + 20 * math.sin(2 * math.pi / self.frames * (frame + 1))), 4)

		elif type == 2:
			pygame.draw.lines(self.screen, (75, 25, 0), False, (
				(x/2, y - 75), 
				(x/2 + side * 15, y - 75 - 7 * math.sin(2 * math.pi / self.frames * (frame + 1))),
				(x/2 + side * 30, y - 75 + 14 * math.sin(2 * math.pi / self.frames * (frame + 1))),
				(x/2 + side * 35, y - 75 - 20 * math.sin(2 * math.pi / self.frames * (frame + 1))),
				), 4)

		pygame.draw.circle(self.screen, (255, 255, 255), (x / 2, y - 30), 30)
		pygame.draw.circle(self.screen, (255, 255, 255), (x / 2, y - 75), 20)
		pygame.draw.circle(self.screen, (255, 255, 255), (x / 2, y - 100), 10)
		pygame.draw.polygon(self.screen, (0, 125, 0), (
			(x/2, y - 120), (x/2 - 3, y - 120),
			(x/2 - 3, y - 110), (x/2 - 16, y - 110), 
			(x/2 - 16, y - 105), (x/2 + 16, y - 105),
			(x/2 + 16, y - 110), (x/2 + 3, y - 110),
			(x/2 + 3, y - 120),
		)) 

		# FRONT HAND
		if type == 1:
			pygame.draw.line(self.screen, (75, 25, 0),
				(x/2, y - 75), (x/2 + side * 35, y - 75 - 20 * math.sin(2 * math.pi / self.frames * (frame + 1))), 4)

		elif type == 2:
			pygame.draw.lines(self.screen, (75, 25, 0), False, (
				(x/2, y - 75), 
				(x/2 + side * 15, y - 75 + 7 * math.sin(2 * math.pi / self.frames * (frame + 1))),
				(x/2 + side * 30, y - 75 - 14 * math.sin(2 * math.pi / self.frames * (frame + 1))),
				(x/2 + side * 35, y - 75 + 20 * math.sin(2 * math.pi / self.frames * (frame + 1))),
				), 4)


		# NOSE
		pygame.draw.polygon(self.screen, (250, 160, 0), (
			(x/2 + side * 9, y - 102), 
			(x/2 + side * 9, y - 98), 
			(x/2 + side * 19, y - 100),
		))

		#EYE
		pygame.draw.circle(self.screen, (0, 0, 0), (x/2 + side * 8, y - 102), 2)


if __name__ == "__main__":
	pygame.init()
	clock = pygame.time.Clock()
	screen = pygame.display.set_mode((200, 200))
	pygame.display.set_caption("Animacja")
	snowman = Snowman(screen)
	i = 0
	while True:
		clock.tick(80)
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit()

		screen.fill((0,0,200))
		snowman.draw(i)
		i += 1
		pygame.display.update()
