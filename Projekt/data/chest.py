# -*- encoding: utf8 -*-
# Maciej Szeptuch 2012

import random
import pygame
import field
import scene
import utils

class Chest(field.Field):
	"""Logika skrzynki."""

	def __init__(self, _grid):
		super(Chest, self).__init__(_grid)
		self._modifier = field.MODIFIER_BLOCKED
		self._opened = False

	def setModifier(self, _):
		"""Ignoruje modyfikator, to jest skrzynka."""

		pass

	def putItem(self, _item):
		"""Odłożenie przedmiotu do skrzynki. Maks. 6 przedmiotów."""

		if len(self._items) >= 6:
			return False

		self._items.append(_item)
		return True

	def clicked(self, _scene, _hero):
		"""Otwiera skrzynkę jeśli bohater stoi obok niej."""

		if utils.distance(_hero.getGrid()[:2], self._grid[:2]) > 1:
			return

		if not self._opened: # Przy pierwszym otwarciu generuje zawartość
			self._opened = True
			self._items = [random.choice(scene.AVAILABLE_ITEMS).randomize() for _ in xrange(int(random.gauss(3, 2)) + 1)]

		_scene.chestitems.show(self._items, self._grid, self)

	class Sprite(field.Field.Sprite):
		"""Graficzna reprezentacja skrzynki."""

		def __init__(self, _grid, _logic, _image, _showModifiers = False):
			super(Chest.Sprite, self).__init__(_grid, _logic, 'data/gfx/chest/' + _image + '.png')

class ChestNorth(Chest):
	"""Skrzynka na północnym krańcu pola."""

	class Sprite(Chest.Sprite):
		def __init__(self, _grid, _logic, _showModifiers = False):
			super(ChestNorth.Sprite, self).__init__(_grid, _logic, 'n')

class ChestSouth(Chest):
	"""Skrzynka na południowym krańcu pola."""

	class Sprite(Chest.Sprite):
		def __init__(self, _grid, _logic, _showModifiers = False):
			super(ChestSouth.Sprite, self).__init__(_grid, _logic, 's')

class ChestEast(Chest):
	"""Skrzynka na wschodnim krańcu pola."""

	class Sprite(Chest.Sprite):
		def __init__(self, _grid, _logic, _showModifiers = False):
			super(ChestEast.Sprite, self).__init__(_grid, _logic, 'e')

class ChestWest(Chest):
	"""Skrzynka na zachodnim krańcu pola."""

	class Sprite(Chest.Sprite):
		def __init__(self, _grid, _logic, _showModifiers = False):
			super(ChestWest.Sprite, self).__init__(_grid, _logic, 'w')
