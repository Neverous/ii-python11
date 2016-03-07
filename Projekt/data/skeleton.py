# -*- encoding: utf8 -*-
# Maciej Szeptuch

import random
import utils
from monster import Monster
from arrow import Arrow

class Skeleton(Monster):
	"""Szkielet."""

	def __init__(self, _map, _grid):
		super(Skeleton, self).__init__(_map, _grid, 2, 3, 60, 60, 0, 145)

	def _punch(self):
		"""Atak z łuku."""

		_id = 'skeleton_arrow_' + str(random.randint(0, 1048576))
		_layer = self._map.getLayer('Missiles')
		_layer.add(_id, Arrow(self._map, _layer, _id, self._direction, self._pos))

	class Sprite(Monster.Sprite):
		"""Reprezentacja graficzna szkieletu."""

		def __init__(self, _logic, _layer = None, _id = None):
			self.images = utils.loadImages('data/gfx/skeleton/', alpha = True)
			for _state in ('walk', 'attack'):
				for _direction in ('ne', 'sw'):
					for _d in _direction:
						self.images[_state][_d] = self.images[_state][_direction]

			super(Skeleton.Sprite, self).__init__(_logic, _layer, _id)


