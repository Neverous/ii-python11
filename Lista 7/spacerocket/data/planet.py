# -*- encoding: utf8 -*-

import pygame
from utils import *

MIN_MASS = 170
MAX_MASS = 400
GRAVITY = 6.67384

class Planet(pygame.sprite.Sprite):
	background = None
	def __init__(self, mass, pos):
		super(Planet, self).__init__()

		if not Planet.background:
			Planet.background = loadImage('data/gfx/planet.png', alpha = True)
		
		self.image = pygame.transform.smoothscale(self.background, (200 * mass / MAX_MASS, 281 * mass / MAX_MASS))
		self.rect = self.image.get_rect()
		self.rect.centerx, self.rect.centery = pos
		self.radius = 100 * mass / MAX_MASS
		self.mass = mass

	def getPos(self):
		return self.rect.centerx, self.rect.centery

	def getRadius(self):
		return self.radius
