# -*- encoding: utf8 -*-

import pygame
from utils import *
import map

_graphics = {
	0: '',
	map.DIRECTION_NONE: 'c',
	map.DIRECTION_UP: 'n',
	map.DIRECTION_RIGHT: 'e',
	map.DIRECTION_DOWN: 's',
	map.DIRECTION_LEFT: 'w',
}

class Cursor(pygame.sprite.Sprite):
	images = None
	def __init__(self, _engine, _map):
		super(Cursor, self).__init__()
		if not Cursor.images:
			Cursor.images = loadImages('data/gfx/cursor/', alpha = True)

		self._engine = _engine
		self._map = _map
		self._resx, self._resy = _engine.getResolution()

		pygame.mouse.set_pos((self._resx / 2, self._resy / 2))
		pygame.mouse.set_visible(False)
		#pygame.event.set_grab(True)

		self._pos = pygame.mouse.get_pos()
		self._direction = map.DIRECTION_NONE
		self.updateCursor()
		self.moveCursor()

	def screenUpdated(self):
		self._resx, self._resy = self._engine.getResolution()

	def update(self):
		self._pos = mx, my = pygame.mouse.get_pos()
		self._before = self._direction
		self._direction = 0

		if mx < 16:
			self._direction |= map.DIRECTION_LEFT

		elif self._resx - mx < 16:
			self._direction |= map.DIRECTION_RIGHT

		if my < 16:
			self._direction |= map.DIRECTION_UP

		elif self._resy - my < 16:
			self._direction |= map.DIRECTION_DOWN

		if not self._direction:
			self._direction = map.DIRECTION_NONE

		if self._direction != self._before:
			self.updateCursor()

		if not self._direction & map.DIRECTION_NONE:
			self._map.move(self._direction)

		self.moveCursor()

	def getState(self):
		if self._direction & map.DIRECTION_NONE:
			return _graphics[map.DIRECTION_NONE]

		return _graphics[(self._direction & map.DIRECTION_UP) | (self._direction & map.DIRECTION_DOWN)] + _graphics[(self._direction & map.DIRECTION_LEFT) | (self._direction & map.DIRECTION_RIGHT)]

	def updateCursor(self):
		self.image = self.images[self.getState()]
		self.rect = self.image.get_rect()

	def moveCursor(self):
		self.rect.centerx, self.rect.centery = self._pos

	def draw(self, surface):
		surface.blit(self.image, (self.rect.left, self.rect.top))
