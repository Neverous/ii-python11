# -*- encoding: utf8 -*-
# Maciej Szeptuch 2012

import random
from item import Item

class Armor(Item):
	"""Pancerz."""

	@classmethod
	def randomize(cls):
		"""Zwraca pancerz o losowych własnościach."""

		return Armor(int(random.gauss(5, 2)))

	def __init__(self, _defence):
		super(Armor, self).__init__('data/gfx/armor.png')
		self.stats['defence'] = max(1, _defence)

	def getDescription(self):
		return "Pancerz\nObrona: %d" % (self.stats['defence'])
