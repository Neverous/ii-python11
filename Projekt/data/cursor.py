# -*- encoding: utf8 -*-
# Maciej Szeptuch 2012

import pygame
from pygame.locals import *
import utils
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
	"""Wyświetlanie kursora."""

	def __init__(self, _engine, _map):
		super(Cursor, self).__init__()
		self.images = utils.loadImages('data/gfx/cursor/', alpha = True)

		self._engine = _engine
		self._map = _map
		self._resx, self._resy = _engine.getResolution()

		pygame.mouse.set_pos((self._resx / 2, self._resy / 2))
		pygame.mouse.set_visible(False)

		self._cursor = None
		self._pos = pygame.mouse.get_pos()
		self._direction = map.DIRECTION_NONE
		self._updated = []
		self.updateCursor()
		self.moveCursor()

	def setCursor(self, _name = None):
		"""Ustawia kursor na _name."""

		_before = self._cursor
		self._cursor = _name
		if _before != _name:
			self._updated.append(tuple(self.rect))
			self.updateCursor()
			self._updated.append(tuple(self.rect))

	def getRectangle(self):
		"""Zwraca obszar obsługiwany przez kursor."""

		return pygame.Rect(0, 0, self._resx, self._resy)

	def screenUpdated(self):
		"""Aktualizuje rozdzielczość."""

		self._resx, self._resy = self._engine.getResolution()

	def update(self):
		"""Aktualizuje wygląd kursora i w razie konieczności wymusza przesunięcie mapy."""

		mx, my = self._pos
		self._before = self._direction
		self._direction = 0
		updated = [tuple(self.rect)]

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
		updated.append(self.rect)
		if self._before == self.rect.center:
			updated = []

		updated += self._updated
		self._updated = []
		return updated

	def getState(self):
		"""Zwraca nazwę obrazka kursora."""

		if self._cursor:
			return self._cursor

		if self._direction & map.DIRECTION_NONE:
			return _graphics[map.DIRECTION_NONE]

		return _graphics[(self._direction & map.DIRECTION_UP) | (self._direction & map.DIRECTION_DOWN)] + _graphics[(self._direction & map.DIRECTION_LEFT) | (self._direction & map.DIRECTION_RIGHT)]

	def updateCursor(self):
		"""Aktualizuje obrazek kursora."""

		self.image = self.images[self.getState()]
		self.rect = self.image.get_rect()

	def moveCursor(self):
		"""Przesuwa obrazek kursora w odpowiednie miejsce."""

		self._before = self.rect.center
		self.rect.center = self._pos

	def draw(self, surface):
		"""Rysuje kursor na powierzchni."""

		surface.blit(self.image, self.rect.topleft)

	def mouseEvent(self, _event, _pos):
		"""Obsługa zdarzeń myszy."""

		if _event.type == MOUSEMOTION: # zapamiętywanie pozycji
			self._pos = tuple(_pos)
