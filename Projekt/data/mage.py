# -*- encoding: utf8 -*-
# Maciej Szeptuch

import random
import utils
from monster import Monster
from fireball import Fireball
from iceblast import Iceblast
from heal import Heal

class Mage(Monster):
	"""Mag."""

	def __init__(self, _map, _grid):
		super(Mage, self).__init__(_map, _grid, 3, 3, 180, 40, 210)

	def _punch(self):
		"""Atakuje czarem ognia lub lodu."""

		if random.randint(1, 2) == 1 and (not random.randint(0, 8) or utils.distance(self._grid[:2], self._target.getGrid()[:2]) > 1): # ogniem najlepiej wtedy gdy cel jest daleko
			_id = 'mage_fireball_' + str(random.randint(0, 1048576))
			_layer = self._map.getLayer('Missiles')
			_layer.add(_id, Fireball(self._map, _layer, _id, self._direction, self._pos))

		else:
			_id = 'mage_iceblast_' + str(random.randint(0, 1048576))
			_layer = self._map.getLayer('Missiles')
			_layer.add(_id, Iceblast(self._map, _layer, _id, self._direction, self._pos))

	def update(self):
		if random.randint(1, 3000) == 1 and self.getLife(True) < 1: # raz na jakiś czas możne się uleczyć
			self._attackCounter = 0
			_id = 'mage_heal_' + str(random.randint(0, 1048576))
			_layer = self._map.getLayer('Missiles')
			_layer.add(_id, Heal(self._map, _layer, _id, self._direction, self._pos))
			return False

		return super(Mage, self).update()

	class Sprite(Monster.Sprite):
		"""Reprezentacja graficzna maga."""

		def __init__(self, _logic, _layer = None, _id = None):
			self.images = utils.loadImages('data/gfx/mage/', alpha = True)
			for _direction in ('ne', 'sw'):
				for _d in _direction:
					self.images['walk'][_d] = self.images['walk'][_direction]

			for _d in 'nswe':
				self.images['attack'][_d]['0'] = self.images['walk'][_d]['0']

			super(Mage.Sprite, self).__init__(_logic, _layer, _id)

