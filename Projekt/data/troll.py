# -*- encoding: utf8 -*-
# Maciej Szeptuch

import utils
from monster import Monster

class Troll(Monster):
	"""Trol."""

	def __init__(self, _map, _grid):
		super(Troll, self).__init__(_map, _grid, 1, 1, 240, 200, 0, 500)
		self._sound = utils.loadSound('data/snd/troll.wav')

	def _punch(self):
		self._sound.play()
		self._target.hit(50)

	class Sprite(Monster.Sprite):
		"""Reprezentacja graficzna trola."""

		def __init__(self, _logic, _layer = None, _id = None):
			self.images = utils.loadImages('data/gfx/troll/', alpha = True)
			for _state in ('walk', 'attack'):
				for _direction in ('ne', 'sw'):
					for _d in _direction:
						self.images[_state][_d] = self.images[_state][_direction]

			super(Troll.Sprite, self).__init__(_logic, _layer, _id)


