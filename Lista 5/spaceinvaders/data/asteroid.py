# -*- encoding: utf8 -*-
import sys
import pygame
from pygame.locals import *
from utils import *
class Asteroid(AnimatedSprite):
	images = None
	def __init__(self, game, x, y, health = 700):
		super(Asteroid, self).__init__()
		self.game = game
		self.x = x
		self.y = y
		self.health = health
		if not Asteroid.images:
			Asteroid.images = loadImages('data/gfx/asteroid/', None, True)

		self.step = self.health / len(Asteroid.images)
		self.image = self.images['0']
		self.rect = self.image.get_rect()
		self.rect.centerx, self.rect.centery = self.x, self.y

	def update(self):
		pass

	def hit(self, hit, point):
		self.health -= hit
		if self.health < 0:
			self.health = 0

		self.image = self.images[str(len(self.images) - int(self.health / self.step) - 1)]
		self.rect = self.image.get_rect()
		self.rect.centerx, self.rect.centery = self.x, self.y

