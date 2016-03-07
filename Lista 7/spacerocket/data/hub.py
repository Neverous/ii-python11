# -*- encoding: utf8 -*-

import random
import pygame
from utils import *
import rocket

class Hub(object):
	images = None
	def __init__(self, _engine):
		super(Hub, self).__init__()

		if not Hub.images:
			Hub.images = {
				'health': loadImages('data/gfx/health/', alpha = True),
				'fuel': loadImage('data/gfx/fuel.png', alpha = True),
			}

		self._engine = _engine
		self._resx, self._resy = self._engine.getResolution()
		self._healthandtext = pygame.Surface((self._resx, 64), pygame.SRCALPHA)
		self._fuel = pygame.Surface((self._resx, 64))
		self._fuel.fill((0, 255, 66, 0))
		self._fuel.set_colorkey((0, 255, 66))
		self._i = 0
		self._r = random.randint(0, len(self.images['health']) - 1)

	def screenUpdated(self):
		self._resx, self._resy = self._engine.getResolution()

	def draw(self, surface):
		surface.blit(self._fuel, (0, 0))
		surface.blit(self._healthandtext, (0, 0))

	def update(self):
		self._healthandtext = pygame.Surface((self._resx, 64), pygame.SRCALPHA)
		self._fuel = pygame.Surface((self._resx, 64))
		self._fuel.fill((0, 255, 66, 0))
		self._fuel.set_colorkey((0, 255, 66))
		drawText(self._healthandtext, "Poziom: %(level)d Wynik: %(score)d" % self._engine.game, 13, (255, 255, 255), (self._resx / 2, 15))
		if self._engine.game['godlevel'] == self._engine.game['level']:
			drawText(self._healthandtext, "GOD MODE", 14, (255, 255, 255), (self._resx / 2, 30))

		pygame.draw.rect(self._fuel, (140, 140, 50), (15, 52, 32, -41 * self._engine.game['fuel'] / rocket.MAX_FUEL))
		self._fuel.blit(self.images['fuel'], (15, 10))
		for life in xrange(self._engine.game['life']):
			self._healthandtext.blit(self.images['health'][str((self._i + self._r * life) % len(self.images['health']))], (self._resx - 47 - life * 42, 10))
			
		self._i += 1
		if self._i > 3:
			self._i = 0
