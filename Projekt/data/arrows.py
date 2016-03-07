# -*- encoding: utf8 -*-
# Maciej Szeptuch 2012

import random
from item import Item

class Arrows(Item):
	"""Strzały."""

	@classmethod
	def randomize(cls):
		"""Zwraca losową liczbę strzał."""

		return Arrows(int(random.gauss(8, 2)))

	def __init__(self, _quant = 1):
		super(Arrows, self).__init__('data/gfx/arrow/s.png')
		self.stats['quant'] = max(1, _quant)

	def getDescription(self):
		return "Strzaly\nAtak: 7\nLiczba: %d\n" % self.stats['quant']
