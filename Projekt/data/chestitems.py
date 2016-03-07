# -*- encoding: utf8 -*-
# Maciej Szeptuch 2012

import pygame
from pygame.locals import *
from inventory import Cell
import utils

class ChestItems(object):
	"""Panel wyświetlający przedmioty ze skrzynki."""

	def __init__(self, _engine, _hero, _freeobjs):
		"""_engine - obiekt silnika, _hero - bohater, _freeobjs - wolne obiekty na planie(nie przypisane do żadnej warstwy, panelu)"""

		super(ChestItems, self).__init__()
		self.images = {
			'cell': utils.loadImage('data/gfx/cell.png', alpha = True),
		}

		self._updated = []
		self._engine = _engine
		self._hero = _hero
		self.screenUpdated()
		self.surface = pygame.Surface((192, 192))
		self.surface.fill((1, 5, 4))
		self.surface.set_colorkey((1, 5, 4))
		self._cells = pygame.sprite.Group()
		pygame.draw.rect(self.surface, (0, 0, 0), (0, 7, 192, 2))
		for y in xrange(2):
			for x in xrange(3):
				cell = Cell((x, y), _freeobjs)
				cell.rect.center = (cell.rect.centerx + 8*x, cell.rect.centery + 16 + y*8)
				self._cells.add(cell)

		self._cells.draw(self.surface)
		pygame.draw.rect(self.surface, (0, 0, 0), (120, 20, 64, 64))
		self._chest = None # wskaźnik na otwartą skrzynkę
		self.opened = None # pozycja otwartej skrzynkę

	def getCell(self, _pos):
		"""Zwraca komórkę znajdującą się pod _pos."""

		for cell in self._cells:
			if cell.rect.collidepoint(_pos):
				return cell

		return None

	def getRectangle(self):
		"""Zwraca obszar zajmowany przez panel."""

		return pygame.Rect(self._pos[0], self._pos[1], 192, 88)

	def screenUpdated(self):
		"""Aktualizuje pozycję panelu i wymusza odświeżenie obszaru."""

		self._resx, self._resy = self._engine.getResolution()
		_resx = self._resx
		self._resx = int((self._resx - 200) / 32) * 32
		_pad = (_resx - self._resx - 192) / 2
		self._pos = (self._resx + _pad, 2 * _pad + 408)
		self._refresh = True

	def show(self, _items, _pos, _chest):
		"""Wyświetla daną skrzynkę."""

		for (_cell, _item) in zip(self._cells, _items):
			_item.attach(_cell)

		self.opened = _pos
		self._refresh = True
		self._chest = _chest

	def update(self):
		"""Aktualizowanie klikniętych kafelków/modyfikatorów."""

		updated = [(x + self._pos[0], y + self._pos[1], w, h) for x, y, w, h in self._updated]
		if self.opened and utils.distance(self._hero.getGrid()[:2], self.opened[:2]) > 1:
			for cell in self._cells:
				cell.clear(self._chest)

			self.opened = None
			self._chest = None

		self._updated = []
		for cell in self._cells:
			_upd = cell.update()
			if _upd:
				updated.extend(map(lambda (x, y, w, h): (x + self._pos[0], y + self._pos[1], w, h), _upd))
				cell.draw(self.surface)

		if self._refresh:
			self._refresh = False
			return [tuple(self.getRectangle())]

		return updated

	def draw(self, surface):
		"""Rysuje menu na powierzchni."""

		surface.blit(self.surface, self._pos)

	def mouseEvent(self, _event, _pos = None):
		"""Obsługa zdarzeń myszy."""

		if not _pos:
			return

		if _event.type == MOUSEMOTION: # Rysowanie opisu przedmiotu
			pygame.draw.rect(self.surface, (0, 0, 0), (120, 20, 64, 64))
			self._updated.append((120, 20, 64, 64))
			for cell in self._cells:
				if cell.rect.collidepoint(_pos):
					_item = cell.getItem()
					if _item:
						utils.drawText(self.surface, _item.getDescription(), 8, (255, 255, 255), (152, 52))

					break

		for cell in self._cells:
			if cell.rect.collidepoint(_pos):
				cell.mouseEvent(_event)
