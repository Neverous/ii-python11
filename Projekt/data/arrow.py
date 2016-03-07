# -*- encoding: utf8 -*-
# Maciej Szeptuch 2012

import utils
from map import HoverLayer, MAP_SIZE
import field

# PRĘDKOŚĆ LOTU

SPEED = 5

class Arrow(HoverLayer.Sprite):
	"""Wystrzelona strzała."""

	def __init__(self, _map, _layer, _id, _direction, _start, _modifier = 1):
		self.images = utils.loadImages('data/gfx/arrow/', alpha = True)
		super(Arrow, self).__init__(self.images[_direction])
		self._modifier = _modifier # Modyfikator siły ataku
		self._map = _map
		self._layer = _layer
		self._id = _id
		self._vec = (_direction == 's' and (0, SPEED)) or (_direction == 'n' and (0, -SPEED)) or (_direction == 'e' and (SPEED, 0)) or (-SPEED, 0) # Wektor ruchu
		self._pos = _start[0] + self._vec[0] / SPEED * 17, _start[1] + self._vec[1] / SPEED * 17 # Aktualna pozycja
		self._start = _start

	def update(self):
		self._layer.clear(self._id)
		self._pos = self._pos[0] + self._vec[0], self._pos[1] + self._vec[1]
		self.move(self._pos)
		return super(Arrow, self).update()

	def move(self, _pos):
		"""Obsługuje ruch i kolizje strzały."""

		if not 0 <= _pos[0] <= MAP_SIZE * 32 or not 0 <= _pos[1] <= MAP_SIZE * 32: # poza mapą
			self._layer.clear(self._id)
			self.kill()
			return

		if utils.distance(self._start, _pos) > 32 * 5: # dolatuje na odległość 5 kratek
			self._layer.clear(self._id)
			self.kill()
			return

		_field = self._map.getLayer('Fields').get(_pos).getLogic()
		if _field.getModifier() & field.MODIFIER_BLOCKED:
			self._layer.clear(self._id)
			self.kill()
			return

		if _field.getOccupied():
			_field.getOccupied().hit(7 * self._modifier)
			self._layer.clear(self._id)
			self.kill()
			return

		super(Arrow, self).move(_pos)
