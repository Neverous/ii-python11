# -*- encoding: utf8 -*-
# Maciej Szeptuch 2012

import math
import random
import pygame
from collections import defaultdict
from map import HoverLayer
import utils
import scene
import field

# PRĘDKOŚĆ ANIMACJI
ANIMATION_SPEED = 2

class Creature(object):
	"""Logika stwora."""

	def __init__(self, _map, _grid, _speed = 4, _life = 30, _mana = 10, _experience = 50):
		super(Creature, self).__init__()
		self._map = _map
		self.stats = defaultdict(lambda: 0) # statystyki potwora życie itp.
		self._grid = _grid
		self._pos = 32 * _grid[0] + 16, 32 * _grid[1] + 16
		self._dest = None # w kierunku jakiego pola się porusza
		self._refresh = False
		self._speed = _speed
		self._direction = 's'
		self.stats['life'] = _life
		self.stats['maxlife'] = _life
		self.stats['mana'] = _mana
		self.stats['maxmana'] = _mana
		self.stats['experience'] = _experience
		self._dmg = 0 # ilość obrażen zadanych stworowi (zerowane przy każdym sprawdzeniu)

	def getStats(self):
		return dict(self.stats)

	def getMap(self):
		"""Zwraca obiekt mapy na której znajduje się stwór."""

		return self._map

	def getPos(self):
		"""Zwraca aktualną pozycje stwora."""

		return self._pos

	def getGrid(self):
		"""Zwraca adres aktualnie zajmowanego pola."""

		return self._grid

	def getOccupied(self):
		"""Zwraca adres zarezerwowanego pola(pól jeśli się porusza)."""

		return tuple(set((self._grid, (self._pos[0] / 32, self._pos[1] / 32, self._grid[2]))))

	def getDestination(self):
		"""Zwraca docelowe pole."""

		return self._dest

	def getLife(self, relative = False):
		"""Zwraca liczbę punktów życia/procent."""

		if not relative:
			return max(self.stats['life'], 0)

		return min(max(1.0 * self.stats['life'] / self.stats['maxlife'], 0), self.stats['maxlife'])

	def getMana(self, relative = False):
		"""Zwraca liczbę punktów many/procent."""

		if not relative:
			return max(self.stats['mana'], 0)

		return min(max(1.0 * self.stats['mana'] / self.stats['maxmana'], 0), self.stats['maxmana'])

	def getSprite(self, _layer, _id):
		"""Zwraca reprezentacje graficzną stwora. UWAGA: za każdym wywołaniem tworzy nowy obiekt!"""

		return self.Sprite(self, _layer, _id)

	def getDirection(self):
		"""Zwraca zwrot stwora."""

		if not self._dest:
			return self._direction

		if self._dest[0] * 32 + 16 > self._pos[0]:
			self._direction = 'e'

		elif self._dest[0] * 32 + 16 < self._pos[0]:
			self._direction = 'w'

		elif self._dest[1] * 32 + 16 > self._pos[1]:
			self._direction = 's'

		elif self._dest[1] * 32 + 16 < self._pos[1]:
			self._direction = 'n'

		return self._direction

	def setDirection(self, _direction):
		"""Ustawia zwrot."""

		if self._direction == _direction:
			return

		self._direction = _direction
		self._refresh = True

	def getDamage(self):
		"""Zwraca odniesione obrażenia od ostatniego zapytania."""

		_dmg = self._dmg
		self._dmg = 0
		return _dmg

	def heal(self, _points):
		"""Uzdrawia stwora (chyba że nie żyje)."""

		if self.stats['life'] <= 0:
			return

		self.stats['life'] = min(self.stats['life'] + _points, self.stats['maxlife'])

	def manaplus(self, _points):
		"""Przywraca punkty many stwora."""

		self.stats['mana'] = min(self.stats['mana'] + _points, self.stats['maxmana'])

	def hit(self, _points):
		"""Obsługuje uderzenie stwora."""

		self.stats['life'] -= _points
		self._dmg += _points

	def move(self, _vec):
		"""Wprawia stworzenie w ruch w kierunku danego pola."""

		_dest = self._grid[0] + _vec[0], self._grid[1] + _vec[1], self._grid[2] + _vec[2]
		if _vec[2]: # jeśli ruszamy się w z to znaczy że wchodzimy po schodach
			self._map.getLayer('Fields').get(self._pos).getLogic().occupy(None)
			self._grid = _dest
			self._pos = 32 * self._grid[0] + 16, 32 * self._grid[1] + 16
			self._dest = None
			return

		if self._dest: # nie ma pola docelowego = brak ruchu
			return

		_field = self._map.getLayer('Fields').get((_dest[0] * 32 + 16, _dest[1] * 32 + 16))
		if not _field: # brak pola = brak ruchu
			return
		
		_field = _field.getLogic()
		if _field.getModifier() & field.MODIFIER_BLOCKED or not _field.getOccupied() in (None, self): # pole zablokowane, bądź zajęte przez kogoś innego
			return

		_field.occupy(self)
		self._dest = _dest

	def update(self):
		"""Aktualizuje stworzenie."""

		if self._dest:
			self._refresh = False
			self._move()
			return True

		if self._refresh:
			self._refresh = False
			return True

		return False

	def _move(self):
		"""Porusza stworem."""

		_sqrt = 0
		_pos = list(self._pos)
		for v in xrange(2):
			if self._dest[v] - self._grid[v]:
				_sqrt += 1

		if _sqrt:
			_speed = self._speed / math.sqrt(_sqrt)

		else:
			_speed = self._speed

		for v in xrange(2):
			if _pos[v] < self._dest[v] * 32 + 16:
				_pos[v] = min(_pos[v] + _speed, self._dest[v] * 32 + 16)

			elif _pos[v] > self._dest[v] * 32 + 16:
				_pos[v] = max(_pos[v] - _speed, self._dest[v] * 32 + 16)

		if self._dest[0] * 32 + 16 == _pos[0] and self._dest[1] * 32 + 16 == _pos[1]:
			self._dest = None

		self._pos = tuple(_pos)
		_before = self._grid
		self._grid = int(self._pos[0] / 32), int(self._pos[1] / 32), self._grid[2]
		if _before != self._grid:
			self._map.getLayer('Fields').get((_before[0] * 32 + 16, _before[1] * 32 + 16)).getLogic().occupy(None)
			self._map.getLayer('Fields').get(self._pos).getLogic().entered(self)

	def kill(self):
		"""Obsługuje śmierć stwora."""

		_field = self._map.getLayer('Fields').get(self._pos).getLogic()
		_field.occupy(None)
		if random.randint(0, 100) < 15: # 15 % szans
			_item = random.choice(scene.AVAILABLE_ITEMS).randomize()
			_item.attach(_field)

		self._pos = (-1000, -1000)
		self._grid = (-1000, -1000, -1000)

	class Sprite(HoverLayer.Sprite):
		"""Reprezentacja graficzna stwora."""

		def __init__(self, _logic, _layer = None, _id = None):
			super(Creature.Sprite, self).__init__()
			self._logic = _logic
			self._layer = _layer
			self._id = _id
			self._refresh = True
			self._state = 'walk'
			self._frame = 0
			self._counter = 0
			self._cnt = 0
			self.image = self.getImage()
			self.damage = pygame.Surface((32, 32), pygame.SRCALPHA) # powierzchnia do wypisywania odniesionych obrażeń
			self.rect = self.image.get_rect()
			self.rect.center = self._logic.getPos()

		def kill(self):
			"""Zabija stwora."""

			self._layer.clear(self._id)
			self.getLogic().kill()
			super(Creature.Sprite, self).kill()

		def getGrid(self):
			"""Zwraca pozycje stwora na siatce."""

			return self._logic.getGrid()

		def getPos(self):
			"""Zwraca rzeczywistą pozycje stwora."""

			return self._logic.getPos()

		def getLogic(self):
			"""Zwraca obiekt logiki."""

			return self._logic

		def getDirection(self):
			"""Zwraca kierunek w którym zwrócone jest stworzenie."""

			return self._logic.getDirection()

		def getState(self):
			"""Zwraca stan obrazka."""

			return self._state

		def update(self):
			"""Aktualizuje obrazek."""

			if not self.getLogic().getLife(): # jeśli nie żyje to trzeba go wyrzucić z puli
				self.kill()
				return []

			_destination = self._logic.getDestination()
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
				return [list(self.rect)]

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

		def getImage(self):
			"""Zwraca aktualny obrazek potwora."""

			_frame = str(self._frame)
			self._counter += 1
			if self._counter >= 10/ANIMATION_SPEED:
				self._frame += 1
				self._counter = 0

			if self.images[self.getState()][self.getDirection()][str(self._frame)] == {}:
				self._frame = 0

			return self.images[self.getState()][self.getDirection()][_frame]

		def draw(self, surface):
			"""Rysuje stwora na powierzchni."""

			if not self.getLogic().getLife():
				return

			surface.blit(self.image, self.rect.topleft)
			surface.blit(self.damage, self.rect.topleft)
