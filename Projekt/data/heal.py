# -*- encoding: utf8 -*-
# Maciej Szeptuch 2012

import utils
from map import HoverLayer

# PRĘDKOŚĆ ANIMACJI
ANIMATION_SPEED = 1

class Heal(HoverLayer.Sprite):
	"""Czar uzdrawiania."""

	def __init__(self, _map, _layer, _id, _, _pos, _modifier = 1):
		self.images = utils.loadImages('data/gfx/heal/', alpha = True)
		super(Heal, self).__init__(self.images['0'])
		self._map = _map
		self._layer = _layer
		self._id = _id
		self._pos = _pos
		self.rect.center = self._pos
		self._frame = 1
		self._counter = 0
		self._last = 60
		_field = self._map.getLayer('Fields').get(_pos)
		if _field: # uzdrawianie stwora na danym polu
			_mns = _field.getLogic().getOccupied()
			if _mns:
				_mns.heal(_modifier * 100)

	def nextFrame(self):
		"""Ustawia następną klatkę animacji."""

		self._counter += 1
		_frame = self._frame
		if self._counter >= 15/ANIMATION_SPEED:
			self._frame += 1
			self._counter = 0

		if self.images[str(self._frame)] == {}:
			self._frame = 0

		self.changeImage(self.images[str(_frame)])

	def update(self):
		self._last -= 1
		self._layer.clear(self._id)
		if not self._last:
			self.kill()
			return

		self.nextFrame()
		return super(Heal, self).update()
