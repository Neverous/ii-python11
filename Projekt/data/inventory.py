# -*- encoding: utf8 -*-
# Maciej Szeptuch 2012

import pygame
from pygame.locals import *
from map import HoverLayer
import utils
from shield import Shield
from weapon import Weapon
from armor import Armor
from potion import Potion
import arrows

class Inventory(object):
	"""Panel ekwipunku."""

	def __init__(self, _engine, _hero, _inventory, _freeobjs):
		"""_engine - obiekt silnika, _inventory - ekwipunek  bohatera, _hero - bohater, _freeobjs - wolne obiekty na scenie(nie przypisane do żadnej warstwy)"""

		super(Inventory, self).__init__()
		self.images = {
			'cell': utils.loadImage('data/gfx/cell.png', alpha = True),
		}

		self._updated = []
		self._engine = _engine
		self._hero = _hero
		self._inventory = _inventory
		self.screenUpdated()
		self.surface = pygame.Surface((192, 192))
		self.surface.fill((1, 5, 4))
		self.surface.set_colorkey((1, 5, 4))
		self._cells = pygame.sprite.Group()
		for y in xrange(2, 5):
			for x in xrange(5):
				cell = Cell((x, y), _freeobjs, self._hero)
				cell.rect.center = (cell.rect.centerx + 8*x, cell.rect.centery + y*8)
				self._cells.add(cell)

		for (_cell, _item) in zip(self._cells, _inventory):
			_item.attach(_cell)

		_cell = LeftHandCell((0, 0), _freeobjs, self._hero) # lewa ręka
		_cell.rect.center = (_cell.rect.centerx, _cell.rect.centery)
		self._cells.add(_cell)

		_cell = ArmorCell((1, 0), _freeobjs, self._hero) # pancerz
		_cell.rect.center = (_cell.rect.centerx + 8, _cell.rect.centery)
		self._cells.add(_cell)

		_cell = RightHandCell((2, 0), _freeobjs, self._hero) #prawa ręka
		_cell.rect.center = (_cell.rect.centerx + 16, _cell.rect.centery)
		self._cells.add(_cell)

		_cell = StrengthCell((0, 1), self._hero) # Siła
		_cell.rect.center = (_cell.rect.centerx, _cell.rect.centery + 8)
		self._cells.add(_cell)

		_cell = IntelligenceCell((1, 1), self._hero) # Inteligencja
		_cell.rect.center = (_cell.rect.centerx + 8, _cell.rect.centery + 8)
		self._cells.add(_cell)

		_cell = AgilityCell((2, 1), self._hero) # Zręczność
		_cell.rect.center = (_cell.rect.centerx + 16, _cell.rect.centery + 8)
		self._cells.add(_cell)

		self._cells.draw(self.surface)
		pygame.draw.rect(self.surface, (0, 0, 0), (120, 4, 64, 64))

	def add(self, _item):
		"""Dodaje przedmiot do ekwipunku."""

		for _cell in self._cells:
			if type(_cell) == Cell and not _cell.getItem():
				_item.attach(_cell)
				return

	def getCell(self, _pos):
		"""Zwraca komórke pod _pos."""

		for cell in self._cells:
			if cell.rect.collidepoint(_pos):
				return cell

		return None

	def getRectangle(self):
		"""Zwraca obszar zajmowany przez menu."""

		return pygame.Rect(self._pos[0], self._pos[1], 192, 192)

	def screenUpdated(self):
		"""Aktualizuje pozycję menu i wymusza odświeżenie obszaru."""

		self._resx, self._resy = self._engine.getResolution()
		_resx = self._resx
		self._resx = int((self._resx - 200) / 32) * 32
		_pad = (_resx - self._resx - 192) / 2
		self._pos = (self._resx + _pad, 2 * _pad + 208)
		self._refresh = True

	def update(self):
		"""Aktualizowanie klikniętych kafelków/modyfikatorów."""

		updated = [(x + self._pos[0], y + self._pos[1], w, h) for x, y, w, h in self._updated]
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

		if _event.type == MOUSEMOTION: # aktualizuje opisy przedmiotów
			pygame.draw.rect(self.surface, (0, 0, 0), (120, 4, 64, 64))
			self._updated.append((120, 4, 64, 64))
			for cell in self._cells:
				if cell.rect.collidepoint(_pos):
					_item = cell.getItem()
					if _item:
						utils.drawText(self.surface, _item.getDescription(), 8, (255, 255, 255), (152, 36))

					break

		for cell in self._cells:
			if cell.rect.collidepoint(_pos):
				cell.mouseEvent(_event)

		if _event.type == MOUSEBUTTONDOWN and _event.button == 3: # Używanie mikstur prawym przyciskiem myszy
			for cell in self._cells:
				if cell.rect.collidepoint(_pos):
					_item = cell.getItem()
					if isinstance(_item, Potion):
						_item.use(self._hero)
	
					break

class Cell(pygame.sprite.Sprite):
	"""Komórka w ekwipunku."""

	def __init__(self, _grid, _freeobjs = None, _hero = None):
		"""_grid - pozycja pola na siatce, _modifier - modyfikator."""

		super(Cell, self).__init__()
		self.image = utils.loadImage('data/gfx/cell.png', alpha = True)
		self._freeobjs = _freeobjs
		self._grid = _grid
		self._hero = _hero
		self.rect = self.image.get_rect()
		self.rect.center = _grid[0] * 32 + 16, _grid[1] * 32 + 16
		self._refresh = True
		self._item = None

	def clear(self, _chest = None):
		if self._item:
			_item = self._item
			_item.detach()
			_item.attach(_chest)
			self._item = None
			self._refresh = True

	def getGrid(self):
		"""Zwraca pozycje pola na siatce."""

		return self._grid

	def draw(self, surface):
		"""Rysuje reprezentacje modyfikatora na danej powierzchni."""

		surface.blit(self.image, self.rect.topleft)
		if self._item:
			surface.blit(self._item.image, self.rect.topleft)

	def update(self):
		if self._refresh:
			self._refresh = False
			return [tuple(self.rect)]

		return []

	def mouseEvent(self, _event):
		if _event.type == MOUSEBUTTONDOWN and _event.button == 1 and self._item:
			self._freeobjs.add(self._item)
			self._item.detach()
			self._item = None
			self._refresh = True

	def putItem(self, _item):
		if type(self._item) == type(_item) and type(_item) == arrows.Arrows:
			self._item.stats['quant'] += _item.stats['quant']
			_item.kill()
			return True

		if not self._item:
			self._item = _item
			if self._hero:
				self._hero.inventory.add(_item)

			self._refresh = True
			return True

		return False

	def gotItem(self):
		self._freeobjs.add(self._item)
		if self._hero:
			self._hero.inventory.remove(self._item)

		self._item = None
		self._refresh = True

	def getItem(self):
		return self._item

class LeftHandCell(Cell):
	def __init__(self, _grid, _freeobjs, _hero):
		super(LeftHandCell, self).__init__(_grid, _freeobjs)
		self.image = utils.loadImage('data/gfx/handcell.png', alpha = True)
		self._hero = _hero

	def putItem(self, _item):
		if not isinstance(_item, (Weapon, Shield)):
			return False

		for stat in ('defence', 'attack', 'speed', 'distance'):
			self._hero.stats[stat] += _item.stats[stat]

		return super(LeftHandCell, self).putItem(_item)

	def gotItem(self):
		self._freeobjs.add(self._item)
		if self._hero:
			self._hero.inventory.remove(self._item)
			for stat in ('defence', 'attack', 'speed', 'distance'):
				self._hero.stats[stat] -= self._item.stats[stat]

		self._item = None
		self._refresh = True

class ArmorCell(Cell):
	def __init__(self, _grid, _freeobjs, _hero):
		super(ArmorCell, self).__init__(_grid, _freeobjs)
		self.image = utils.loadImage('data/gfx/armorcell.png', alpha = True)
		self._hero = _hero

	def putItem(self, _item):
		if not isinstance(_item, Armor):
			return False

		for stat in ('defence', 'attack', 'speed', 'distance'):
			self._hero.stats[stat] += _item.stats[stat]

		return super(ArmorCell, self).putItem(_item)

	def gotItem(self):
		self._freeobjs.add(self._item)
		if self._hero:
			self._hero.inventory.remove(self._item)
			for stat in ('defence', 'attack', 'speed', 'distance'):
				self._hero.stats[stat] -= self._item.stats[stat]

		self._item = None
		self._refresh = True

class RightHandCell(Cell):
	def __init__(self, _grid, _freeobjs, _hero):
		super(RightHandCell, self).__init__(_grid, _freeobjs)
		self.image = utils.loadImage('data/gfx/handcell.png', alpha = True)
		self._hero = _hero

	def putItem(self, _item):
		if not isinstance(_item, (Weapon, Shield)):
			return False

		for stat in ('defence', 'attack', 'speed', 'distance'):
			self._hero.stats[stat] += _item.stats[stat]

		return super(RightHandCell, self).putItem(_item)

	def gotItem(self):
		self._freeobjs.add(self._item)
		if self._hero:
			self._hero.inventory.remove(self._item)
			for stat in ('defence', 'attack', 'speed', 'distance'):
				self._hero.stats[stat] -= self._item.stats[stat]

		self._item = None
		self._refresh = True

class StrengthCell(Cell):
	def __init__(self, _grid, _hero):
		super(StrengthCell, self).__init__(_grid)
		self.image = utils.loadImage('data/gfx/strengthcell.png', alpha = True)
		self._hero = _hero
		self._before = 0
		utils.drawText(self.image, "Sila", 9, (0, 0, 0), (16, 6))

	def update(self):
		if self._hero.stats['points'] != self._before:
			self._before = self._hero.stats['points']
			return [tuple(self.rect)]

		return super(StrengthCell, self).update()

	def draw(self, surface):
		surface.blit(self.image, self.rect.topleft)
		utils.drawText(surface, str(self._hero.stats['strength']) + '%', 12, (255, 255, 255), (self.rect.centerx, self.rect.centery + 6))
		if self._hero.stats['points']:
			utils.drawText(surface, '+', 14, (255, 0, 0), (self.rect.right - 7, self.rect.bottom - 7))

	def mouseEvent(self, _event):
		if _event.type == MOUSEBUTTONDOWN and _event.button == 1 and self._hero.stats['points']:
			self._hero.stats['strength'] += 4
			self._hero.stats['points'] -= 1
			self._refresh = True

	def putItem(self, _item):
		return False

class IntelligenceCell(Cell):
	def __init__(self, _grid, _hero):
		super(IntelligenceCell, self).__init__(_grid)
		self.image = utils.loadImage('data/gfx/intelligencecell.png', alpha = True)
		self._hero = _hero
		self._before = 0
		utils.drawText(self.image, "Inteligencja", 9, (0, 0, 0), (16, 6))

	def putItem(self, _item):
		return False

	def update(self):
		if self._hero.stats['points'] != self._before:
			self._before = self._hero.stats['points']
			return [tuple(self.rect)]

		return super(IntelligenceCell, self).update()

	def draw(self, surface):
		surface.blit(self.image, self.rect.topleft)
		utils.drawText(surface, str(self._hero.stats['intelligence']) + '%', 12, (255, 255, 255), (self.rect.centerx, self.rect.centery + 6))
		if self._hero.stats['points']:
			utils.drawText(surface, '+', 14, (255, 0, 0), (self.rect.right - 7, self.rect.bottom - 7))

	def mouseEvent(self, _event):
		if _event.type == MOUSEBUTTONDOWN and _event.button == 1 and self._hero.stats['points']:
			self._hero.stats['intelligence'] += 4
			self._hero.stats['points'] -= 1
			self._refresh = True

class AgilityCell(Cell):
	def __init__(self, _grid, _hero):
		super(AgilityCell, self).__init__(_grid)
		self.image = utils.loadImage('data/gfx/agilitycell.png', alpha = True)
		self._hero = _hero
		self._before = 0
		utils.drawText(self.image, "Zrecznosc", 9, (0, 0, 0), (16, 6))

	def putItem(self, _item):
		return False

	def update(self):
		if self._hero.stats['points'] != self._before:
			self._before = self._hero.stats['points']
			return [tuple(self.rect)]

		return super(AgilityCell, self).update()

	def draw(self, surface):
		surface.blit(self.image, self.rect.topleft)
		utils.drawText(surface, str(self._hero.stats['agility']) + '%', 12, (255, 255, 255), (self.rect.centerx, self.rect.centery + 6))
		if self._hero.stats['points']:
			utils.drawText(surface, '+', 14, (255, 0, 0), (self.rect.right - 7, self.rect.bottom - 7))

	def mouseEvent(self, _event):
		if _event.type == MOUSEBUTTONDOWN and _event.button == 1 and self._hero.stats['points']:
			self._hero.stats['agility'] += 4
			self._hero.stats['points'] -= 1
			self._refresh = True
