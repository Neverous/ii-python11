# -*- encoding: utf8 -*-
# Maciej Szeptuch

import utils
from monster import Monster

class Spider(Monster):
	"""Pająk."""

	def __init__(self, _map, _grid):
		super(Spider, self).__init__(_map, _grid, 1, 1, 120, 20, 0, 70)

	def _punch(self):
		self._target.hit(3)

	class Sprite(Monster.Sprite):
		"""Reprezentacja graficzna pająka."""

		def __init__(self, _logic, _layer = None, _id = None):
			self.images = utils.loadImages('data/gfx/spider/', alpha = True)
			for _d in 'nswe':
				self.images['attack'][_d]['0'] = self.images['walk'][_d]['0']

			super(Spider.Sprite, self).__init__(_logic, _layer, _id)


