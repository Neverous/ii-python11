# -*- encoding: utf8 -*-
# Maciej Szeptuch 2012

import pygame
from pygame.locals import *
from map import MapLayer

class MinimapLayer(MapLayer):
	"""Warstwa minimapy."""

	def __init__(self, _map):
		super(MinimapLayer, self).__init__(_map)
		self.surface = pygame.Surface((192, 192))
		self.hidden = True

	def update(self):
		"""Aktualizuje minimapę."""

		_fields = self._map.getLayer('Fields')
		_shadow = self._map.getLayer('Shadow')
		if _shadow and _shadow.check():
			pygame.transform.scale(_fields.surface, (192, 192), self.surface)
			_shadow = pygame.transform.smoothscale(_shadow.surface, (192, 192))
			self.surface.blit(_shadow, (0, 0))
			self._check = True

		elif _fields and _fields.check():
			pygame.transform.scale(_fields.surface, (192, 192), self.surface)
			if _shadow:
				_shadow = pygame.transform.smoothscale(_shadow.surface, (192, 192))
				self.surface.blit(_shadow, (0, 0))

			self._check = True

		return []

class Minimap(object):
	"""Minimapa."""

	def __init__(self, _engine, _map):
		"""_engine - obiekt silnika, _map - obiekt mapy."""

		super(Minimap, self).__init__()
		self._engine = _engine
		self._map = _map
		self._layer = MinimapLayer(_map)
		self.surface = self._layer.surface
		self._map.addLayer('Minimap', 1000, self._layer)
		self._x, self._y = 1, 1
		self._refresh = True
		self._frame = pygame.Surface((192, 192))
		self._frame.set_colorkey((0, 0, 0))
		self._mapsize = _map.getSize()
		self._moving = False
		self.screenUpdated()

	def getRectangle(self):
		"""Zwraca obszar zajmowany przez minimapę."""

		return pygame.Rect(self._pos[0], self._pos[1], 192, 192)

	def screenUpdated(self):
		"""Aktualizuje pozycję minimapy i wymusza odświeżenie obszaru."""

		self._resx, self._resy = self._engine.getResolution()
		_resx = self._resx
		self._resx = self._map.getRectangle().width
		_pad = (_resx - self._resx - 192) / 2
		self._pos = (self._resx + _pad, _pad)
		self._window = (self._resx * 192 / self._mapsize[0], self._resy * 192 / self._mapsize[1])
		self._refresh = True

	def mouseEvent(self, _event, _pos):
		"""Obsługa zdarzeń myszy."""

		if _event.type == MOUSEBUTTONUP and _event.button == 1:
			self._moving = False
			return

		if not _pos:
			return

		if self._moving and _event.type == MOUSEMOTION:
			self.move(_pos)

		if _event.type == MOUSEBUTTONDOWN and _event.button == 1:
			self._moving = True
			self.move(_pos)
			return

	def move(self, _pos):
		"""Przesuwa mapę odpowiednio w zależności od _pos."""

		mw, mh = self._mapsize
		x, y = _pos[0] - self._window[0] / 2, _pos[1] - self._window[1] / 2
		x, y = -x * mw / 192, -y * mh / 192
		self._map.setShift((x, y))

	def update(self):
		"""Aktualizuje pozycję ramki."""

		x, y = self._map.getShift()
		_check = self._layer.check()
		if not _check and not self._refresh and (self._x, self._y) == (x, y):
			return []

		mw, mh = self._mapsize
		_before = (self._pos[0] + -self._x * 192 / mw, self._pos[1] + -self._y * 192 / mh, self._window[0], self._window[1])
		self._x, self._y = x, y
		self._frame.fill((0, 0, 0))
		x, y = -x * 192 / mw, -y * 192 / mh
		_after = (self._pos[0] + x, self._pos[1] + y, self._window[0], self._window[1])
		pygame.draw.rect(self._frame, (255, 0, 0), (x, y, self._window[0], self._window[1]), 1)

		if _check or self._refresh:
			self._refresh = False
			return [(self._pos[0], self._pos[1], 198, 192)]

		return [_before, _after]

	def draw(self, surface):
		"""Rysuje minimapę na powierzchni."""

		for l in xrange(1, self._map.getStoreys() + 1):
			pygame.draw.rect(surface, l == self._map.getStorey() + 1 and (255, 255, 255) or (128, 128, 128), (self._pos[0] + 193, self._pos[1] + 5 * l, 5, 3))

		surface.blit(self.surface, self._pos)
		surface.blit(self._frame, self._pos)
