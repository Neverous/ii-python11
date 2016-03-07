# -*- encoding: utf8 -*-

import pygame
from utils import *

class Canister(AnimatedSprite):
	images = None
	def __init__(self, pos):
		super(Canister, self).__init__(pos)

		if not Canister.images:
			Canister.images = loadImages('data/gfx/canister/', alpha = True)
		
		self.image = Canister.images['0']
		self.rect = self.image.get_rect()
		self.rect.centerx, self.rect.centery = pos
		self.radius = 16
		self.mass = 30
		self._i = 0

	def getPos(self):
		return self.rect.centerx, self.rect.centery

	def getRadius(self):
		return self.radius

	def update(self):
		self._i += 1
		if self._i > 6:
			self._i = 0

		if not self._i:
			self.nextFrame(Canister.images)
