# -*- encoding: utf8 -*-
# Maciej Szeptuch 2012

import pygame
import engine
import field

class Wall(field.Field):
	"""Logika ściany."""

	def __init__(self, _grid):
		super(Wall, self).__init__(_grid)
		self._modifier = field.MODIFIER_BLOCKED

	def setModifier(self, _):
		"""Ignoruje modyfikator, to jest ściana."""

		pass

	def putItem(self, _item):
		"""Zawsze zwraca fałsz. Na ścianie nie można nic położyć."""
		
		return False

	class Sprite(field.Field.Sprite):
		"""Graficzna reprezentacja ściany."""

		def __init__(self, _grid, _logic, _image, _showModifiers = False):
			super(Wall.Sprite, self).__init__(_grid, _logic, 'data/gfx/wall/' + _image + '.png')

class WallHorizontal(Wall):
	"""Pozioma ściana."""

	class Sprite(Wall.Sprite):
		def __init__(self, _grid, _logic, _showModifiers = False):
			super(WallHorizontal.Sprite, self).__init__(_grid, _logic, 'h')

class WallVertical(Wall):
	"""Pionowa ściana."""

	class Sprite(Wall.Sprite):
		def __init__(self, _grid, _logic, _showModifiers = False):
			super(WallVertical.Sprite, self).__init__(_grid, _logic, 'v')

class WallTopLeft(Wall):
	"""Ściana w lewym górnym rogu."""

	class Sprite(Wall.Sprite):
		def __init__(self, _grid, _logic, _showModifiers = False):
			super(WallTopLeft.Sprite, self).__init__(_grid, _logic, 'tl')

class WallTopRight(Wall):
	"""Ściana w prawym górnym rogu."""

	class Sprite(Wall.Sprite):
		def __init__(self, _grid, _logic, _showModifiers = False):
			super(WallTopRight.Sprite, self).__init__(_grid, _logic, 'tr')

class WallBottomLeft(Wall):
	"""Ściana w lewym dolnym rogu."""

	class Sprite(Wall.Sprite):
		def __init__(self, _grid, _logic, _showModifiers = False):
			super(WallBottomLeft.Sprite, self).__init__(_grid, _logic, 'bl')

class WallBottomRight(Wall):
	"""Ściana w prawym dolnym rogu."""

	class Sprite(Wall.Sprite):
		def __init__(self, _grid, _logic, _showModifiers = False):
			super(WallBottomRight.Sprite, self).__init__(_grid, _logic, 'br')
