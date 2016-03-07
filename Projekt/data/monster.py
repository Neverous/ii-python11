# -*- encoding: utf8 -*-
# Maciej Szeptuch 2012

import random
import pygame
import utils
from creature import Creature
import field
import hero

class Monster(Creature):
	"""Potwór - stwór z AI."""

	def __init__(self, _map, _grid, _speed = 5, _attackDistance = 1, _attackSpeed = 30, _life = 50, _mana = 30, _experience = 50):
		super(Monster, self).__init__(_map, _grid, _speed, _life, _mana, _experience)
		self._reference = _grid
		self._attackDistance = _attackDistance
		self._target = None
		self._attackCounter = 0
		self._attackSpeed = _attackSpeed

	def setReference(self, _reference):
		"""Ustawia punkt względem którego potwór się porusza."""

		self._reference = _reference

	def getTarget(self):
		"""Czy atakuje?"""

		return self._target

	def update(self):
		"""Aktualizuje stworzenie."""

		if self._target:
			self._refresh = False
			self._attack()
			return True

		if self._dest:
			self._refresh = False
			self._move()
			return True

		_level = self._map.getLevel(self._grid[2])
		try:
			_inrange = filter(lambda (_x, _y): type(_level[_y][_x].getOccupied()) == hero.Hero, utils.neighbours(self._grid[:2], lambda (_x, _y): not _level[_y][_x].getModifier() & field.MODIFIER_BLOCKED, 4))[0]
		
		except IndexError:
			_inrange = None
		
		# atakuj bohatera
		if _inrange:
			_vec = _inrange[0] - self._grid[0], _inrange[1] - self._grid[1]

		if _inrange and utils.distance(_inrange, self._grid[:2]) <= self._attackDistance and not (_vec[0] and _vec[1]):
			self._direction = (_vec[0] > 0 and 'e') or (_vec[0] < 0 and 'w') or (_vec[1] > 0 and 's') or 'n'
			self._target = _level[_inrange[1]][_inrange[0]].getOccupied()
		
		# lub rusz sie w jego kierunku
		elif _inrange:
			try:
				_vec = utils.shortPath(self._grid[:2], _inrange, lambda (_x, _y): not _level[_y][_x].getModifier() & field.MODIFIER_BLOCKED and (not _level[_y][_x].getOccupied() or type(_level[_y][_x].getOccupied()) == hero.Hero))[1]
				_vec = _vec[0] - self._grid[0], _vec[1] - self._grid[1], 0
				self.move(_vec)

			except IndexError:
				_vec = (
					(1, 0, 0),
					(-1, 0, 0),
					(0, 1, 0),
					(0, -1, 0),
				)

				_vec = filter(lambda _v: (self._grid[0] + _v[0] - self._reference[0]) ** 2 + (self._grid[1] + _v[1] - self._reference[1]) ** 2 <= 16, _vec)
				try:
					self.move(random.choice(_vec))

				except IndexError:
					pass # NO POSSIBLE MOVES

		# lub losowy ruch w okolicy
		else:
			_vec = (
				(1, 0, 0),
				(-1, 0, 0),
				(0, 1, 0),
				(0, -1, 0),
			)

			_vec = filter(lambda _v: (self._grid[0] + _v[0] - self._reference[0]) ** 2 + (self._grid[1] + _v[1] - self._reference[1]) ** 2 <= 16, _vec)
			try:
				self.move(random.choice(_vec))

			except IndexError:
				pass # NO POSSIBLE MOVES

		if self._refresh:
			self._refresh = False
			return True

		return False

	def _attack(self):
		"""Atakuje cel."""

		if not self._target:
			return

		_vec = self._target.getGrid()[0] - self._grid[0], self._target.getGrid()[1] - self._grid[1]
		if utils.distance(self._grid[:2], self._target.getGrid()[:2]) > self._attackDistance or (_vec[0] and _vec[1]):
			self.setReference(self._grid)
			self._target = None
			return

		self._attackCounter += 1
		if self._attackCounter >= self._attackSpeed:
			self._attackCounter = 0
			self._punch()

	def _punch(self):
		"""Uderzenie."""

		pass

	class Sprite(Creature.Sprite):
		"""Reprezentacja potwora."""

		def __init__(self, _logic, _layer = None, _id = None):
			super(Monster.Sprite, self).__init__(_logic, _layer, _id)
			_logic.setReference(_logic.getGrid())

		def update(self):
			"""Aktualizuje obrazek."""

			if not self.getLogic().getLife():
				self.kill()
				return []

			_destination = self._logic.getDestination()
			_attack = self._logic.getTarget()
			if _attack and self._state != 'attack':
				self._state = 'attack'
				self._frame = 0

			if _destination and self._state != 'walk':
				self._state = 'walk'
				self._frame = 0

			if self._state == 'walk' and not _destination:
				self._frame = 0

			if self._logic.update() or self._refresh:
				if self._layer:
					self._layer.clear(self._id)

				self.image = self.getImage()
				self.rect.center = self._logic.getPos()

				self._refresh = False
				return [tuple(self.rect)]

			self._cnt += 1
			if self._cnt == 90:
				self._cnt = 0
				self.damage.fill((0, 0, 0, 0))

			_dmg = self._logic.getDamage()
			if _dmg:
				self.damage.fill((0, 0, 0, 0))
				utils.drawText(self.damage, "%d" % _dmg, 10, (255, 120, 120), (16, 8))
				return [tuple(self.rect)]

			return []

		def draw(self, surface):
			"""Rysuje stwora na powierzchni."""

			if not self.getLogic().getLife():
				return

			surface.blit(self.image, self.rect.topleft)
			pygame.draw.rect(surface, (0, 0, 0), (self.rect.left + 4, self.rect.top + 2, 24, 4)) 
			if self.getLogic().getLife(True):
				pygame.draw.rect(surface, (0, 255, 0), (self.rect.left + 5, self.rect.top + 3, self._logic.getLife(True) * 22, 2)) 

			surface.blit(self.damage, self.rect.topleft)
