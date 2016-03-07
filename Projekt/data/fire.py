# -*- encoding: utf8 -*-
# Maciej Szeptuch 2012

import utils
from map import HoverLayer

# PRĘDKOŚĆ ANIMACJI
ANIMATION_SPEED = 3

class Fire(HoverLayer.Sprite):
	"""Ogień."""

	def __init__(self, _map, _layer, _id, _pos, _modifier = 1):
		self.images = utils.loadImages('data/gfx/fire/', alpha = True)
		super(Fire, self).__init__(self.images['0'])
		self._map = _map
		self._layer = _layer
		self._id = _id
		self._pos = int(_pos[0] / 32) * 32 + 16, int(_pos[1] / 32) * 32 + 16
		self.rect.center = self._pos
		self._modifier = _modifier
		self._frame = 0
		self._counter = 0
		self._last = 60 # Czas spalania

	def nextFrame(self):
		"""Ustawia następną ramkę animacji."""

		self._counter += 1
		if self._counter >= 10/ANIMATION_SPEED:
			self._frame += 1
			self._counter = 0

		if self.images[str(self._frame)] == {}:
			self._frame = 0

		self.changeImage(self.images[str(self._frame)])

	def update(self):
		_field = self._map.getLayer('Fields').get(self._pos)
		if _field and self._last % 15 == 0: # raz na 15 klatek atakuje znajdujące się na polu stworzenie
			_target = _field.getLogic().getOccupied()
			if _target:
				_target.hit(self._modifier * 8)

		self._last -= 1
		self._layer.clear(self._id)
		if not self._last:
			self.kill()
			return

		self.nextFrame()
		return super(Fire, self).update()
