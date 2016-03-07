# -*- encoding: utf8 -*-
# Maciej Szeptuch 2012

import random
from weapon import Weapon

class Axe(Weapon):
	"""Topór."""

	@classmethod
	def randomize(cls):
		"""Zwraca topór o losowych właściwościach."""

		return Axe(int(random.gauss(10, 6)), max(0, random.gauss(1.5, 1)))

	def __init__(self, _attack = 1, _speed = 2):
		super(Axe, self).__init__(_attack, _speed, 'data/gfx/axe.png')

	def getDescription(self):
		return "Topor\nAtak: %d\nSzybkosc: %.2f" % (self.stats['attack'], 1.0/self.stats['speed'])
