# -*- encoding: utf8 -*-
# Maciej Szeptuch 2012

import utils
from map import HoverLayer

# PRĘDKOŚĆ ANIMACJI
ANIMATION_SPEED = 1

class Iceblast(HoverLayer.Sprite):
	"""Lodowy podmuch."""

	def __init__(self, _map, _layer, _id, _direction, _pos, _modifier = 1):
		self.images = utils.loadImages('data/gfx/iceblast/', alpha = True)
		super(Iceblast, self).__init__(self.images[_direction]['0'])
		self._sound = utils.loadSound('data/snd/ice.wav')
		self._map = _map
		self._layer = _layer
		self._id = _id
		self._direction = _direction
		self._pos = int(_pos[0] / 32) * 32 + 16 + ((_direction == 'e' and 1) or (_direction == 'w' and -1) or 0) * 64, int(_pos[1] / 32) * 32 + 16 + ((_direction == 's' and 1) or (_direction == 'n' and -1) or 0) * 64
		self.rect.center = self._pos
		self._modifier = _modifier
		self._frame = 0
		self._counter = 0
		self._last = 40
		self._sound.play()

	def nextFrame(self):
		"""Ustawia następną klatkę animacji."""

		self._counter += 1
		_frame = self._frame
		if self._counter >= 20/ANIMATION_SPEED:
			self._frame += 1
			self._counter = 0

		if self.images[self._direction][str(self._frame)] == {}:
			self._frame = 0

		self.changeImage(self.images[self._direction][str(_frame)])

	def update(self):
		"""Aktualizuje obrazek i zadaje obrażenia."""

		self._last -= 1
		self._layer.clear(self._id)
		if not self._last:
			self.kill()
			return

		self.nextFrame()
		if not self._counter:
			_pos = self._pos
			_layer = self._map.getLayer('Fields')
			_field = _layer.get(_pos)
			if _field:
				_mns = _field.getLogic().getOccupied()
				if _mns:
					_mns.hit(10 * self._modifier)

			# im dalej od źródła tym mniej obrażeń
			for (i, j, _d) in ((-1, 0, 'e'), (1, 0, 'w'), (0, -1, 's'), (0, 1, 'n')):
				if self._direction == _d:
					_field = _layer.get((_pos[0] + i * 32, _pos[1] + j * 32))
					if _field:
						_mns = _field.getLogic().getOccupied()
						if _mns:
							_mns.hit(20 * self._modifier)

			for (i, j, _d) in ((2, 0, 'e'), (-2, 0, 'w'), (0, 2, 's'), (0, -2, 'n')):
				if self._direction == _d:
					_field = _layer.get((_pos[0] + i * 32, _pos[1] + j * 32))
					if _field:
						_mns = _field.getLogic().getOccupied()
						if _mns:
							_mns.hit(5 * self._modifier)

		return super(Iceblast, self).update()
