# -*- encoding: utf8 -*-
import pygame
import engine
import field

class Stairs(field.Field):
	"""Logika schodów."""

	def __init__(self, _grid, _direction = 1):
		super(Stairs, self).__init__(_grid)
		self._direction = _direction

	def setModifier(self, _):
		"""Ignoruje modyfikator, to są schody."""

		pass

	def putItem(self, _item):
		"""Zawsze zwraca fałsz. Na schodach nie można nic położyć."""
		
		return False

	def entered(self, _creature):
		"""Przemieszcza stwora na kolejny poziom labiryntu."""

		_creature.move((0, 0, self._direction))

	class Sprite(field.Field.Sprite):
		"""Graficzna reprezentacja schodów."""

		def __init__(self, _grid, _logic, _image, _showModifiers = False):
			super(Stairs.Sprite, self).__init__(_grid, _logic, 'data/gfx/stairs/' + _image + '.png')

class StairsUp(Stairs):
	"""Logika schodów prowadzących do góry."""

	def __init__(self, _grid):
		super(StairsUp, self).__init__(_grid, -1)

class StairsDown(Stairs):
	"""Logika schodów prowadzących w dół."""

	def __init__(self, _grid):
		super(StairsDown, self).__init__(_grid, 1)

class StairsUpNorth(StairsUp):
	"""Schody do góry północ."""

	class Sprite(StairsUp.Sprite):
		def __init__(self, _grid, _logic, _showModifiers = False):
			super(StairsUpNorth.Sprite, self).__init__(_grid, _logic, 'un')

class StairsDownNorth(StairsDown):
	"""Schody w dół północ."""

	class Sprite(StairsDown.Sprite):
		def __init__(self, _grid, _logic, _showModifiers = False):
			super(StairsDownNorth.Sprite, self).__init__(_grid, _logic, 'dn')

class StairsUpSouth(StairsUp):
	"""Schody do góry południe."""

	class Sprite(StairsUp.Sprite):
		def __init__(self, _grid, _logic, _showModifiers = False):
			super(StairsUpSouth.Sprite, self).__init__(_grid, _logic, 'us')

class StairsDownSouth(StairsDown):
	"""Schody w dół południe."""

	class Sprite(StairsDown.Sprite):
		def __init__(self, _grid, _logic, _showModifiers = False):
			super(StairsDownSouth.Sprite, self).__init__(_grid, _logic, 'ds')

class StairsUpEast(StairsUp):
	"""Schody do góry wschód."""

	class Sprite(StairsUp.Sprite):
		def __init__(self, _grid, _logic, _showModifiers = False):
			super(StairsUpEast.Sprite, self).__init__(_grid, _logic, 'ue')

class StairsDownEast(StairsDown):
	"""Schody w dół wschód."""

	class Sprite(StairsDown.Sprite):
		def __init__(self, _grid, _logic, _showModifiers = False):
			super(StairsDownEast.Sprite, self).__init__(_grid, _logic, 'de')

class StairsUpWest(StairsUp):
	"""Schody do góry zachód."""

	class Sprite(StairsUp.Sprite):
		def __init__(self, _grid, _logic, _showModifiers = False):
			super(StairsUpWest.Sprite, self).__init__(_grid, _logic, 'uw')

class StairsDownWest(StairsDown):
	"""Schody w dół zachód."""

	class Sprite(StairsDown.Sprite):
		def __init__(self, _grid, _logic, _showModifiers = False):
			super(StairsDownWest.Sprite, self).__init__(_grid, _logic, 'dw')
