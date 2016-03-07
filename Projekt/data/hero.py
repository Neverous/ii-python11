# -*- encoding: utf8 -*-
# Maciej Szeptuch

import random
from pygame.locals import *
import utils
from creature import Creature
from fireball import Fireball
from iceblast import Iceblast
from heal import Heal
from arrow import Arrow
import arrows

## KLAWISZE RUCHU

DIRECTION_KEYS = (K_w, K_s, K_a, K_d)

## KLAWISZE MAGII

MAGIC_KEYS = (K_1, K_2, K_3)

## MAGIA

MAGIC_FIRE	= 1
MAGIC_ICE	= 2
MAGIC_HEAL	= 4

## Przypisanie klawiszy

KEY_MAP = {
	K_w: (0, -1, 0),
	K_s: (0, 1, 0),
	K_a: (-1, 0, 0),
	K_d: (1, 0, 0),
	K_1: MAGIC_FIRE,
	K_2: MAGIC_ICE,
	K_3: MAGIC_HEAL,
}

## DOŚWIADCZENIE (liczba potrzebnych pkt exp, bonus zdrowia, bonus many, punkty umiejętności)
EXPERIENCE_STEP = (
	(100, 5, 1, 2),
	(200, 5, 1, 2),
	(400, 5, 1, 2),
	(1000, 10, 5, 3),
	(2000, 10, 5, 3),
	(5000, 10, 5, 3),
	(10000, 10, 5, 3),
	(20000, 20, 10, 4),
)


class Hero(Creature):
	"""Bohater."""

	def __init__(self, _map, _grid, _speed = 4, _life = 30, _mana = 10, _experience = 50):
		super(Hero, self).__init__(_map, _grid, _speed, _life, _mana, _experience)
		self._sound = utils.loadSound('data/snd/sword.wav')
		self._spell = MAGIC_FIRE
		self.stats['attack'] = 10
		self.stats['strength'] = self.stats['intelligence'] = self.stats['agility'] = 25
		self.stats['speed'] = 1
		self._attackCounter = 40
		self._regenCounter = 80
		self.inventory = set()

	def hit(self, _points):
		"""Obsługa przyjmowania obrażeń - osłabia zgodznie ze statystykami bohatera."""

		_points = max(1, _points - (5 + self.stats['defence']) * self.stats['strength'] / 100)
		super(Hero, self).hit(_points)

	def addExperience(self, _exp):
		"""Obsługa zdobywania doświadczenia."""

		_before = self.stats['experience']
		self.stats['experience'] += _exp
		for _step, _life, _mana, _points in EXPERIENCE_STEP:
			if _before < _step <= self.stats['experience']:
				self.stats['maxlife'] += _life
				self.stats['life'] = self.stats['maxlife']
				self.stats['maxmana'] += _mana
				self.stats['mana'] = self.stats['maxmana']
				self.stats['points'] += _points

	def setSpell(self, _spell):
		"""Ustawia czar na _spell."""

		self._spell = _spell

	def getDirection(self):
		return self._direction

	def getSpell(self):
		return self._spell

	def castSpell(self):
		if self._attackCounter > 0:
			return

		if self.stats['mana'] < 7:
			return

		self.stats['mana'] -= 7 # Każdy czar kosztuje 7 many
		self._attackCounter = 40
		_modifier = (self.stats['intelligence'] * 67 + self.stats['agility'] * 33) / 10000.0
		if self._spell & MAGIC_ICE:
			_id = 'hero_iceblast_' + str(random.randint(0, 1048576))
			_layer = self._map.getLayer('Missiles')
			_layer.add(_id, Iceblast(self._map, _layer, _id, self._direction, self._pos, _modifier))

		elif self._spell & MAGIC_FIRE:
			_id = 'hero_fireball_' + str(random.randint(0, 1048576))
			_layer = self._map.getLayer('Missiles')
			_layer.add(_id, Fireball(self._map, _layer, _id, self._direction, self._pos, _modifier))

		elif self._spell & MAGIC_HEAL:
			_id = 'hero_heal_' + str(random.randint(0, 1048576))
			_layer = self._map.getLayer('Missiles')
			_layer.add(_id, Heal(self._map, _layer, _id, self._direction, self._pos, _modifier))

	def punch(self):
		if self._attackCounter > 0:
			return

		self._attackCounter = 40 * self.stats['speed']
		if self.stats['distance']: # atak dystansowy(łuk)
			for item in self.inventory:
				if type(item) == arrows.Arrows:
					item.stats['quant'] -= 1
					if not item.stats['quant']:
						item.detach()
						item.kill()

					break

			else:
				return

			_id = 'hero_arrow_' + str(random.randint(0, 1048576))
			_layer = self._map.getLayer('Missiles')
			_layer.add(_id, Arrow(self._map, _layer, _id, self._direction, self._pos, (self.stats['agility'] * 33 + self.stats['strength'] * 67 + self.stats['attack']) / 10000.0))
			return

		# atak wręcz
		_level = self._map.getLevel(self._grid[2])
		_target = None
		try:
			if self._direction == 'n':
				_target = _level[self._grid[1] - 1][self._grid[0]].getOccupied()

			if self._direction == 's':
				_target = _level[self._grid[1] + 1][self._grid[0]].getOccupied()

			if self._direction == 'e':
				_target = _level[self._grid[1]][self._grid[0] + 1].getOccupied()

			if self._direction == 'w':
				_target = _level[self._grid[1]][self._grid[0] - 1].getOccupied()

			if _target == self:
				_target = None

		except:
			pass

		if not _target:
			return

		self._sound.play()
		_target.hit(self.stats['strength'] * self.stats['attack'] / 100)

	def update(self):
		self._attackCounter -= 1
		self._regenCounter -= 1
		if self._regenCounter <= 0: # regeneracja zdrowia i many
			self.heal(3 * self.stats['strength'] / 100)
			self.manaplus(3 * self.stats['intelligence'] / 100)
			self._regenCounter = 80

		return super(Hero, self).update()

	class Sprite(Creature.Sprite):
		"""Reprezentacja graficzna bohatera."""

		def __init__(self, _logic, _layer = None, _id = None):
			self.images = utils.loadImages('data/gfx/hero/', alpha = True)
			self.images['attack'] = self.images['walk']
			super(Hero.Sprite, self).__init__(_logic, _layer, _id)
