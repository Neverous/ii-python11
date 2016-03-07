# -*- encoding: utf8 -*-
# Maciej Szeptuch 2012

import random
from weapon import Weapon

class Bow(Weapon):
	"""Łuk."""

	@classmethod
	def randomize(cls):
		"""Zwraca łuk o losowych właściwościach."""

		return Bow(random.gauss(1.5, 1))

	def __init__(self, _bonus = 0):
		super(Bow, self).__init__(_bonus, 1, 'data/gfx/bow.png')
		self.stats['distance'] = True

	def getDescription(self):
		return "Luk\nBonus: %.2f" % (self.stats['attack'])
