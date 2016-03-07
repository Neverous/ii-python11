# -*- ecoding: utf8 -*-

import pygame
from utils import *
import tank

FREQUENCY = 5

class Workshop(pygame.sprite.Sprite):
	def __init__(self, _pos):
		super(Workshop, self).__init__()
		self._pos = _pos
		self.rect = pygame.Rect(0, 0, 32, 32)
		self.rect.centerx, self.rect.centery = _pos
		self.occupied = None
		self.i = 0

	def getPos(self):
		return self._pos

	def update(self):
		if self.occupied and not pygame.sprite.collide_rect(self, self.occupied):
			self.occupied.repair = False
			self.occupied = None

		if self.occupied and not self.i % FREQUENCY:
			self.occupied.health = min(self.occupied.health + 4, tank.MAX_HEALTH)
			self.occupied.missiles = min(self.occupied.missiles + 1, tank.MAX_MISSILES)
			self.occupied.updateImage()

		self.i += 1
		if self.i == FREQUENCY:
			self.i = 0
