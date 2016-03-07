# -*- encoding: utf8 -*-
# Maciej Szeptuch 2012

import random
import pygame
import utils
from item import Item

class Shield(Item):
	"""Tarcza."""

	@classmethod
	def randomize(cls):
		"""Zwraca tarczę o losowych własnościach."""

		return Shield(int(random.gauss(8, 2)))

	def __init__(self, _defence):
		super(Shield, self).__init__('data/gfx/shield.png')
		self.stats['defence'] = _defence

	def getDescription(self):
		return "Tarcza\nObrona: %d" % self.stats['defence']
