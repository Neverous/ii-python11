# -*- encoding: utf8 -*-

import pygame
from utils import *
from minimap import Minimap

class Hub(pygame.sprite.Sprite):
	background = None
	def __init__(self, _engine, _map):
		super(Hub, self).__init__()
		if not Hub.background:
			Hub.background = loadImage('data/gfx/hub.png', alpha = True)

		self._engine = _engine
		self._map = _map
		self._minimap = Minimap(_engine, _map)
		self.screenUpdated()
		self.image = self.background.copy()
		self.rect = self.image.get_rect()

	def screenUpdated(self):
		self._resx, self._resy = self._engine.getResolution()
		self._minimap.screenUpdated()

	def draw(self, surface):
		surface.blit(self.image, (self.rect.left, self.rect.top))

	def update(self):
		self.rect.centerx = self._resx / 2
		self.image = self.background.copy()
		drawText(self.image, "%02d:%02d" % self._engine.timeLeft(), 13, (255, 255, 255), (40, 10))
		drawText(self.image, "%02d fps" % self._engine.clock.get_fps(), 13, (255, 255, 255), (100, 10))
		drawText(self.image, "Czolgi: %2d" % len(self._engine.players[0]['tanks']), 13, (255, 255, 255), (200, 10))
		drawText(self.image, "Czolgi: %2d" % len(self._engine.players[1]['tanks']), 13, (255, 255, 255), (680, 10))
		drawText(self.image, "%d : %d" % (self._engine.players[0]['score'], self._engine.players[1]['score']), 13, (255, 255, 255), (420, 10))
		self._minimap.update()
		self._minimap.draw(self.image, (748, 10))
