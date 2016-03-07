# -*- encoding: utf8 -*-
# Maciej Szeptuch 2012

import pygame
import engine

## KIERUNKI

DIRECTION_NONE	= 1
DIRECTION_UP	= 2
DIRECTION_RIGHT	= 4
DIRECTION_DOWN	= 8
DIRECTION_LEFT	= 16

## SZYBKOŚĆ PORUSZANIA MAPĄ

SLIDE_SPEED		= 15

## WIELKOŚĆ MAPY

MAP_SIZE		= 32

class Map(object):
	"""Wyświetlanie lochu."""

	def __init__(self, _engine, _scene, _level, _showModifiers = False):
		super(Map, self).__init__()
		self._engine = _engine
		self._showModifiers = _showModifiers # pokazywanie modyfikatorów dla edytora
		self._scene = _scene
		self._level = _level
		self._shift = [0, 0]
		self._storey = 0
		self._refresh = True
		self._size = 32 * MAP_SIZE, 32 * MAP_SIZE
		self.surface = pygame.Surface(self._size)
		self._ordered = []
		self._layers = {}
		self.addLayer('Fields', -1, FieldsLayer(self, self._getStorey()))
		self.screenUpdated()

	def updateLevel(self, _level):
		"""Aktualizuje reprezentacje poziomu. UWAGA: nie aktualizuje wyświetlanej warstwy jeśli aktualny poziom się zmienił należy jeszcze wywołać switchLevel(0)!"""

		self._level = _level

	def getLevel(self, _storey):
		"""Zwraca poziom lochu."""

		return self._level[_storey]

	def getShift(self):
		"""Zwraca przesunięcie mapy."""

		return tuple(self._shift)

	def getSize(self):
		"""Zwraca szerokość i wysokość mapy(w px)."""

		return self._size

	def getRectangle(self):
		"""Zwraca obszar zajmowany przez mapę."""

		return pygame.Rect(0, 0, self._resx, self._resy)

	def getStoreys(self):
		"""Zwraca liczbe poziomów lochu."""

		return len(self._level)

	def getStorey(self):
		"""Zwraca aktualny poziom lochu."""

		return self._storey

	def _getStorey(self):
		"""Zwraca sprite'y aktualnego poziomu."""

		return pygame.sprite.Group([[field.getSprite(self._showModifiers) for field in row] for row in self._level[self._storey]])

	def mouseEvent(self, _event, _pos = None):
		"""Obsługa zdarzeń myszy."""

		if _pos:
			_pos = _pos[0] - self._shift[0], _pos[1] - self._shift[1]

		for layer, _ in reversed(self._ordered):
			if not layer.mouseEvent(_event, _pos):
				break

	def setShift(self, _shift):
		"""Ustawia przesuniecie mapy."""

		_before = list(self._shift)
		if not self._holdpos[0]:
			self._shift[0] = _shift[0]

		if not self._holdpos[1]:
			self._shift[1] = _shift[1]

		self.move(DIRECTION_NONE)
		self._refresh = self._shift != _before

	def switchStorey(self, _step):
		"""Zmienia poziom lochu."""

		self._storey = (self._storey + _step) % len(self._level)
		self.removeLayer('Fields')
		self.addLayer('Fields', -1, FieldsLayer(self, self._getStorey()))

	def screenUpdated(self):
		"""Aktualizuje wyświetlany obszar i w razie konieczności blokuje przesuwanie na osiach."""

		self._resx, self._resy = self._engine.getResolution()
		self._resx = int((self._resx - 200) / 32) * 32
		self._holdpos = [False, False]
		_mw, _mh = self.getSize()
		if self._resx > _mw:
			self._holdpos[0] = True
			self._shift[0] = (self._resx - _mw) / 2

		if self._resy > _mh:
			self._holdpos[1] = True
			self._shift[1] = (self._resy - _mh) / 2

		self._holdpos = tuple(self._holdpos)
		self._refresh = True

	def move(self, direction):
		"""Przesuwa mapę."""

		_before = list(self._shift)
		_mw, _mh = self.getSize()
		if not self._holdpos[0]:
			if direction & DIRECTION_LEFT:
				self._shift[0] += SLIDE_SPEED

			elif direction & DIRECTION_RIGHT:
				self._shift[0] -= SLIDE_SPEED

			self._shift[0] = max(min(0, self._shift[0]), -_mw + self._resx)

		if not self._holdpos[1]:
			if direction & DIRECTION_UP:
				self._shift[1] += SLIDE_SPEED

			elif direction & DIRECTION_DOWN:
				self._shift[1] -= SLIDE_SPEED

			self._shift[1] = max(min(0, self._shift[1]), -_mh + self._resy)

		self._refresh = self._shift != _before

	def update(self):
		"""Aktualizuje warstwy."""

		if self.getStorey() >= self.getStoreys():
			self._storey = self.getStoreys() - 1
			self.switchStorey(0)

		updated = []
		for layer, _ in self._ordered:
			updated.extend(map(lambda (x, y, w, h): pygame.Rect(x + self._shift[0], y + self._shift[1], w, h).clip(self.getRectangle()), layer.update()))
			layer.draw(self.surface, (-self._shift[0], -self._shift[1], self._resx, self._resy))

		if self._refresh:
			self._refresh = False
			return [self.getRectangle()]

		return updated

	def getLayer(self, _name):
		"""Zwraca daną warstwę."""

		if _name in self._layers:
			return self._layers[_name][0]

		return None

	def removeLayer(self, _name):
		"""Usuwa warstwę."""

		self._ordered.remove(self._layers[_name])
		del self._layers[_name]

	def addLayer(self, _name, _priority, _layer):
		"""Dodaje warstwę."""

		self._layers[_name] = (_layer, _priority)
		_pos = 0
		while _pos < len(self._ordered):
			if self._ordered[_pos][1] > _priority:
				break

			_pos += 1

		self._ordered.insert(_pos, (_layer, _priority))

	def draw(self, surface):
		"""Rysuje mape na powierzchni."""

		surface.blit(self.surface, (0, 0), (-self._shift[0], -self._shift[1], self._resx, self._resy))

class MapLayer(object):
	"""Warstwa mapy."""

	def __init__(self, _map, _sprites = None):
		super(MapLayer, self).__init__()
		self._map = _map
		self.surface = pygame.Surface(_map.getSize(), pygame.SRCALPHA)
		self.hidden = False
		self._sprites = _sprites or pygame.sprite.Group()
		self._updated = []
		self._refresh = True
		self._check = True

	def mouseEvent(self, _event, _pos = None):
		"""Zdarzenie myszy, zwraca fałsz jeśli ma zatrzymać propagację do niższych warstw."""

		return True

	def update(self):
		"""Aktualizuj elementy warstwy."""

		if self._refresh:
			self._refresh = False
			return [(0, 0) + self.surface.get_size()]

		updated = list(self._updated)
		self._updated = []
		for sprite in self._sprites:
			_upd = sprite.update()
			if _upd:
				updated.extend(_upd)
				sprite.draw(self.surface)

		if updated:
			self._check = True

		return updated

	def draw(self, _surface, rect = None):
		"""Rysuj warstwę na powierzchni."""

		if not self.hidden:
			if not rect:
				_surface.blit(self.surface, (0, 0))

			else:
				_surface.blit(self.surface, rect, rect)

	def toggle(self):
		"""Pokazuj/ukrywa warstwę."""

		self.hidden = not self.hidden

	def check(self):
		"""Zwraca czy nastąpiły zmiany od ostatniego sprawdzenia."""

		_chk = self._check
		self._check = False
		return _chk

class FieldsLayer(MapLayer):
	"""Warstwa pól na mapie."""

	def __init__(self, _map, _sprites = None):
		super(FieldsLayer, self).__init__(_map, _sprites)
		self.surface = pygame.Surface(_map.getSize())

	def get(self, _pos, _relative = False):
		"""Zwraca obiekt pola zajmujący dany punkt."""

		if _relative:
			_shift = self._map.getShift()
			_pos = _pos[0] - _shift[0], _pos[1] - _shift[1]

		for field in self._sprites:
			if field.rect.collidepoint(_pos):
				return field

		return None

	def set(self, _grid, _sprite):
		"""Zmienia pole w miejscu _grid na _sprite."""

		for field in self._sprites:
			if field.getGrid() == _grid:
				del field
				break

		self._sprites.add(_sprite)

class HoverLayer(MapLayer):
	"""Warstwa "wskaźników"."""

	def __init__(self, _map, _grid = False):
		super(HoverLayer, self).__init__(_map, None)
		self._grid = _grid
		self._repr = {}

	def move(self, _id, _pos):
		"""Przesuwa wskaźnik _id do _pos."""

		self.clear(_id)
		if self._grid:
			_field = self._map.getLayer('Fields').get(_pos, True)
			if not _field:
				return

			_pos = _field.rect.center

		else:
			_shift = self._map.getShift()
			_pos = _pos[0] - _shift[0], _pos[1] - _shift[1]

		self._repr[_id].move(_pos)

	def add(self, _id, _sprite):
		"""Dodaje sprite do wskaźników."""

		self._repr[_id] = _sprite
		self._sprites.add(_sprite)

	def remove(self, _id):
		"""Usuwa sprite o _id ze wskaźników."""

		self._sprites.remove(self._repr[_id])
		self.clear(_id)
		del self._repr[_id]

	def get(self, _id):
		"""Zwraca wskażnik _id."""

		return self._repr[_id]

	def clear(self, _id):
		"""Usuwa obrazek _id z warstwy."""

		pygame.draw.rect(self.surface, (0, 0, 0, 0), self._repr[_id].rect)
		self._updated.append(tuple(self._repr[_id].rect))

	class Sprite(pygame.sprite.Sprite):
		"""Podstawowy wskaźnik."""

		def __init__(self, _image = None):
			super(HoverLayer.Sprite, self).__init__()
			self.image = _image or pygame.Surface((0, 0))
			self.rect = self.image.get_rect()
			self._updated = []

		def kill(self):
			"""Usuwa wskaźnik z warstwy."""

			super(HoverLayer.Sprite, self).kill()
			self.rect.center = (-1000, -1000)

		def getPos(self):
			return self.rect.center

		def changeImage(self, _image):
			"""Ustawia nowy obrazek wskaźnika."""

			self.image = _image
			_pos = self.rect.center
			self.rect = self.image.get_rect()
			self.rect.center = _pos
			self._updated.append(tuple(self.rect))

		def move(self, _pos):
			"""Przesuwa wskaźnik w pozycje _pos."""

			self.rect.center = _pos
			self._updated.append(tuple(self.rect))

		def update(self):
			"""Jeśli sprite się przesunął zwraca miejsce w którym się pojawi. Wpp []."""

			updated = list(self._updated)
			self._updated = []
			return updated

		def draw(self, surface, rect = None):
			"""Rysuje sprite na powierzchni."""

			surface.blit(self.image, self.rect.topleft, rect)
