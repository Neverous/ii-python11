# -*- encoding: utf8 -*-
# Maciej Szeptuch 2012

import random
import pygame
import utils
from item import Item

class Potion(Item):
	"""Mikstura."""

	@classmethod
	def randomize(cls):
		return Potion()

	def __init__(self, _image = 'unknown'):
		super(Potion, self).__init__(_image)

	def getDescription(self):
		return "Mikstura"

class ManaPotion(Potion):
	"""Mikstura many."""

	@classmethod
	def randomize(cls):
		return ManaPotion()

	def __init__(self):
		super(ManaPotion, self).__init__('data/gfx/manapotion.png')

	def getDescription(self):
		return "Mikstura many\nprzywraca 50 many"

	def use(self, _hero):
		"""Używa mikstury na _hero."""

		_hero.manaplus(50)
		self.detach()
		self.kill()

class LifePotion(Potion):
	"""Mikstura życia."""

	@classmethod
	def randomize(cls):
		return LifePotion()

	def __init__(self):
		super(LifePotion, self).__init__('data/gfx/lifepotion.png')

	def getDescription(self):
		return "Mikstura zycia\nprzywraca 50 zycia"

	def use(self, _hero):
		"""Używa mikstury na _hero."""

		_hero.heal(50)
		self.detach()
		self.kill()
