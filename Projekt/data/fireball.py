# -*- encoding: utf8 -*-
# Maciej Szeptuch 2012

import random
import utils
from map import HoverLayer, MAP_SIZE
from fire import Fire
import field

# PRĘDKOŚĆ LOTU
SPEED = 5

# PRĘDKOŚĆ ANIMACJI KULI
ANIMATION_SPEED = 3

class Fireball(HoverLayer.Sprite):
	"""Kula ognia."""

	def __init__(self, _map, _layer, _id, _direction, _start, _modifier = 1):
		self.images = utils.loadImages('data/gfx/fireball/', alpha = True)
		super(Fireball, self).__init__(self.images['0'])
		self._sound = utils.loadSound('data/snd/explosion.wav')
		self._map = _map
		self._layer = _layer
		self._id = _id
		self._pos = _start
		self._start = _start
		self._modifier = _modifier
		self._vec = (_direction == 's' and (0, SPEED)) or (_direction == 'n' and (0, -SPEED)) or (_direction == 'e' and (SPEED, 0)) or (-SPEED, 0)
		self._pos = _start[0] + self._vec[0] / SPEED * 17, _start[1] + self._vec[1] / SPEED * 17
		self._frame = 0
		self._counter = 0

	def nextFrame(self):
		"""Zwraca następną ramkę animacji."""

		self._counter += 1
		if self._counter >= 10/ANIMATION_SPEED:
			self._frame += 1
			self._counter = 0

		if self.images[str(self._frame)] == {}:
			self._frame = 0

		self.changeImage(self.images[str(self._frame)])

	def update(self):
		self._layer.clear(self._id)
		self.nextFrame()
		self._pos = self._pos[0] + self._vec[0], self._pos[1] + self._vec[1]
		self.move(self._pos)
		return super(Fireball, self).update()

	def setOnFire(self, _pos):
		"""Wybuch kuli. Zapala okoliczne kratki."""

		self._sound.play()
		for (i, j) in ((-1, 0), (1, 0), (0, 1), (0, -1), (0, 0)):
			if 0 <= _pos[1] + i * 32 < MAP_SIZE * 32 and 0 <= _pos[0] + j * 32 < MAP_SIZE * 32:
				_id = 'fire_' + str(random.randint(0, 1048576))
				self._layer.add(_id, Fire(self._map, self._layer, _id, (_pos[0] + j * 32, _pos[1] + i * 32), self._modifier))

	def move(self, _pos):
		"""Obsługuje ruch kuli."""

		if not 0 <= _pos[0] <= MAP_SIZE * 32 or not 0 <= _pos[1] <= MAP_SIZE * 32:
			self.kill()
			return

		if utils.distance(self._start, _pos) > 32 * 5: # maks. odległość lotu = 5
			self.setOnFire(_pos)
			self.kill()
			return

		_field = self._map.getLayer('Fields').get(_pos).getLogic()
		if _field.getModifier() & field.MODIFIER_BLOCKED:
			self.setOnFire(_pos)
			self.kill()
			return

		if _field.getOccupied():
			self.setOnFire(_pos)
			self.kill()
			return

		super(Fireball, self).move(_pos)
