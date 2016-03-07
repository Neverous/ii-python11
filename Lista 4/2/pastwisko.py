# -*- encoding: utf8 -*-
# 2012
# Maciej Szeptuch
# II UWr
import sys
import random
import time
import pygame
from pygame.locals import *
from utils import *
from cow import Cow
from shepherd import Shepherd

class Game:
	def __init__(self, cowCount, shepherdCount):
		width = random.randint(100, 200)
		height = random.randint(60, 120)
		pos = (random.randint(1, 640 - width), random.randint(1, 480 - height))
		self.farm = (pos, (width, height))
		self.cows = [Cow(c, self) for c in range(cowCount)]
		self.shepherds = [Shepherd(s, self) for s in range(shepherdCount)]
		self.shepherd = random.randint(0, shepherdCount - 1)
		self.result = (0, cowCount)
		self.start = time.time()

	def getTime(self):
		seconds = int(time.time() - self.start) % 3600
		return '%02d:%02d' % (seconds / 60, seconds % 60)

	def changeShepherd(self, next = None):
		if next == None:
			next = (self.shepherd + 1) % len(self.shepherds)

		self.shepherds[self.shepherd].action = 'stop'
		self.shepherd = next

class HUD:
	def __init__(self, game):
		self.game = game
		self.x, self.y = 320, 0
		self.font = pygame.font.Font(pygame.font.get_default_font(), 14)

	def update(self):
		self.time = self.game.getTime()

	def draw(self, screen):
		text = self.font.render("%d/%d %s %d FPS" % (self.game.result[0], self.game.result[1], self.time, self.game.clock.get_fps()), 1, (255, 255, 255))
		width, height = text.get_size()
		pygame.draw.rect(screen, (0, 0, 0), ((self.x - width / 2 - 5, self.y), (width + 10, height + 10))) 
		screen.blit(text, (self.x - width / 2, self.y + 5))

if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode((640, 480))
	pygame.display.set_caption('Pastwisko - The Game')
	pygame.mouse.set_visible(False)
	game = Game(20, 3)
	clock = game.clock = pygame.time.Clock()
	hud = HUD(game)
	cows = pygame.sprite.Group(game.cows)
	shepherds = pygame.sprite.Group(game.shepherds)
	grassland = pygame.Surface((640, 480))
	grassland.fill((70, 200, 10))
	pygame.draw.rect(grassland, (70, 30, 0), game.farm)

	try:
		while True:
			clock.tick(60)
			for event in pygame.event.get():
				if event.type == QUIT:
					raise KeyboardInterrupt()

				if event.type == KEYUP and event.key == K_TAB:
					game.changeShepherd()


			screen.blit(grassland, (0, 0))

			cows.update()
			shepherds.update()

			if game.result[0] == game.result[1]:
				screen.fill((0, 0, 0))
				text = pygame.font.Font(pygame.font.get_default_font(), 32).render("GRATULACJE!", 1, (255, 255, 255))
				screen.blit(text, (200, 50))
				hud.draw(screen)
				pygame.display.update()
				continue

			hud.update()

			cows.draw(screen)
			x, y = map(int, game.shepherds[game.shepherd].getPosition())
			y += 20
			pygame.draw.circle(screen, (255, 0, 0), (x, y), 20)
			shepherds.draw(screen)
			hud.draw(screen)

			pygame.display.update()

	except KeyboardInterrupt:
		pass
