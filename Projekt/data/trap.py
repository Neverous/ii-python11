# -*- encoding: utf8 -*-
# Maciej Szeptuch 2012

import random
import pygame
import engine
import field
from map import MAP_SIZE
from fire import Fire
from iceblast import Iceblast

class Trap(field.Field):
	"""Logika pułapki."""

	def __init__(self, _grid):
		super(Trap, self).__init__(_grid)

	def launch(self, creature):
		pass

	class Sprite(field.Field.Sprite):
		"""Graficzna reprezentacja pułapki."""

		def __init__(self, _grid, _logic, _image, _showModifiers = False):
			super(Trap.Sprite, self).__init__(_grid, _logic, 'data/gfx/trap/' + _image + '.png', _showModifiers)

class TrapArrow(Trap):
	"""Logika pułapki ze strzałami."""

	def launch(self, _creature):
		"""Atakuje stwora strzałami."""

		_creature.hit(7)

class TrapFire(Trap):
	"""Logika pułapki ognia."""

	def launch(self, _creature):
		"""Atakuje stwora ogniem."""

		_pos = self._grid[0] * 32 + 16, self._grid[1] * 32 + 16
		_layer = _creature.getMap().getLayer('Missiles')
		for (i, j) in ((-1, 0), (1, 0), (0, 1), (0, -1), (0, 0)):
			if 0 <= _pos[1] + i * 32 < MAP_SIZE * 32 and 0 <= _pos[0] + j * 32 < MAP_SIZE * 32:
				_id = 'fire_' + str(random.randint(0, 1048576))
				_layer.add(_id, Fire(_creature.getMap(), _layer, _id, (_pos[0] + j * 32, _pos[1] + i * 32)))

class TrapIce(Trap):
	"""Logika pułapki lodu."""

	def launch(self, _creature):
		"""Atakuje stwora lodem."""

		_direction = random.choice(('n', 's', 'w', 'e'))
		_pos = self._grid[0] * 32 + 16, self._grid[1] * 32 + 16
		_pos = _pos[0] + ((_direction == 'e' and -1) or (_direction == 'w' and 1) or 0) * 32, _pos[1] + ((_direction == 's' and -1) or (_direction == 'n' and 1) or 0) * 32
		_id = 'trap_iceblast_' + str(random.randint(0, 1048576))
		_layer = _creature.getMap().getLayer('Missiles')
		_layer.add(_id, Iceblast(_creature.getMap(), _layer, _id, _direction, _pos))

class TrapTouchArrow(TrapArrow):
	"""Logika pułapki dotykowej ze strzałami."""

	def entered(self, _creature):
		"""Aktywuje pułapkę reagując na nacisk stwora."""

		if not self._items:
			self.launch(_creature)

	class Sprite(TrapArrow.Sprite):
		def __init__(self, _grid, _logic, _showModifiers = False):
			super(TrapTouchArrow.Sprite, self).__init__(_grid, _logic, 'ta', _showModifiers)

class TrapMoveArrow(TrapArrow):
	"""Logika pułapki ruchowej ze strzałami."""

	def entered(self, _creature):
		"""Aktywuje pułapkę reagując na ruch stwora."""

		self.launch(_creature)
	
	class Sprite(TrapArrow.Sprite):
		def __init__(self, _grid, _logic, _showModifiers = False):
			super(TrapMoveArrow.Sprite, self).__init__(_grid, _logic, 'ma', _showModifiers)

class TrapTouchFire(TrapFire):
	"""Logika pułapki dotykowej ognia."""

	def entered(self, _creature):
		"""Aktywuje pułapkę reagując na nacisk stwora."""

		if not self._items:
			self.launch(_creature)

	class Sprite(TrapFire.Sprite):
		def __init__(self, _grid, _logic, _showModifiers = False):
			super(TrapTouchFire.Sprite, self).__init__(_grid, _logic, 'tf', _showModifiers)

class TrapMoveFire(TrapFire):
	"""Logika pułapki ruchowej ognia."""

	def entered(self, _creature):
		"""Aktywuje pułapkę reagując na ruch stwora."""

		self.launch(_creature)
	
	class Sprite(TrapFire.Sprite):
		def __init__(self, _grid, _logic, _showModifiers = False):
			super(TrapMoveFire.Sprite, self).__init__(_grid, _logic, 'mf', _showModifiers)

class TrapTouchIce(TrapIce):
	"""Logika pułapki dotykowej lodu."""

	def entered(self, _creature):
		"""Aktywuje pułapkę reagując na nacisk stwora."""

		if not self._items:
			self.launch(_creature)

	class Sprite(TrapIce.Sprite):
		def __init__(self, _grid, _logic, _showModifiers = False):
			super(TrapTouchIce.Sprite, self).__init__(_grid, _logic, 'ti', _showModifiers)

class TrapMoveIce(TrapIce):
	"""Logika pułapki ruchowej lodu."""

	def entered(self, _creature):
		"""Aktywuje pułapkę reagując na ruch stwora."""

		self.launch(_creature)
	
	class Sprite(TrapIce.Sprite):
		def __init__(self, _grid, _logic, _showModifiers = False):
			super(TrapMoveIce.Sprite, self).__init__(_grid, _logic, 'mi', _showModifiers)
