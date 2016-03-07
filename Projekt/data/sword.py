# -*- encoding: utf8 -*-
# Maciej Szeptuch 2012

import random
import pygame
import utils
from weapon import Weapon

class Sword(Weapon):
	"""Miecz."""

	@classmethod
	def randomize(cls):
		"""Zwraca miecz o losowych własnościach."""

		return Sword(int(random.gauss(8, 6)), max(0, random.gauss(1.5, 0.5)))

	def __init__(self, _attack = 1, _speed = 2):
		super(Sword, self).__init__(_attack, _speed, 'data/gfx/sword.png')

	def getDescription(self):
		return "Miecz\nAtak: %d\nSzybkosc: %.2f." % (self.stats['attack'], 1.0 / self.stats['speed'])
