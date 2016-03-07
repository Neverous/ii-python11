# -*- encoding: utf8 -*-
# Maciej Szeptuch 2012

import random
import pygame
import utils
from item import Item

class Weapon(Item):
	"""Broń."""

	@classmethod
	def randomize(cls):
		return Weapon()

	def __init__(self, _attack = 1, _speed = 2, _image = 'unknown'):
		super(Weapon, self).__init__(_image)
		self.stats['attack'] = max(1, _attack)
		self.stats['speed'] = max(_speed, 1)

	def getDescription(self):
		return "Bron\nAtak: %d\nSzybkosc: %.2f" % (self.stats['attack'], 1.0/self.stats['speed'])
