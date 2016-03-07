# -*- encoding: utf8 -*-
# Maciej Szeptuch 2012

import pygame
from pygame.locals import *
import engine
import utils
from menu import MenuButton, MenuQuit
from field import Field
from cursor import Cursor
from map import Map, MAP_SIZE
from minimap import Minimap
from tilesgrid import TilesGrid
from field import Field

## LIMIT POZIOMÓW LOCHU

LEVEL_LIMIT = 10

class Editor(engine.Module):
	"""Edytor lochów."""

	def __init__(self, _engine):
		super(Editor, self).__init__(_engine)
		self.side = utils.loadImage('data/gfx/side.png')
		self._background = pygame.Surface((self._resx, self._resy))
		self._background.blit(self.side, (self._resx - 232, self._resy - 1500))
		self.surface = self._background.copy()
		self._level = utils.loadLevel('data/level.dat') or [[[Field((x, y)) for x in xrange(MAP_SIZE)] for y in xrange(MAP_SIZE)]]
		self._map = Map(_engine, self, self._level, True)
		self._cursor = Cursor(_engine, self._map)
		self._minimap = Minimap(_engine, self._map)
		self._tiles = TilesGrid(_engine, self, self._map)
		self._menu = EditorMenu(_engine, self)
		self._submodules = (self._map, self._minimap, self._tiles, self._menu, self._cursor)
		self._refresh = True

	def screenUpdated(self):
		"""Aktualizuje obrazy tła i submoduły."""

		super(Editor, self).screenUpdated()
		self._refresh = True
		self._background = pygame.Surface((self._resx, self._resy))
		self._background.blit(self.side, (self._resx - 232, self._resy - 1500))
		self.surface = pygame.transform.smoothscale(self.surface, (self._resx, self._resy))
		for submodule in self._submodules:
			submodule.screenUpdated()

	def setField(self, _l, _x, _y, _new):
		"""Ustawia pole w pozycji (_x, _y, _l) [_l to poziom lochu] na _new."""

		self._level[_l][_y][_x] = _new
		self._map.getLayer('Fields').set((_x, _y), _new.getSprite(True))

	def saveLevel(self):
		"""Zapisuje poziom na dysku."""

		return utils.saveLevel('data/level.dat', self._level)

	def clearLevel(self):
		"""Tworzy pusty poziom."""

		self._level = [[[Field((x, y)) for x in xrange(MAP_SIZE)] for y in xrange(MAP_SIZE)]]
		self._map = Map(self._engine, self, self._level, True)
		self._cursor = Cursor(self._engine, self._map)
		self._minimap = Minimap(self._engine, self._map)
		self._tiles = TilesGrid(self._engine, self, self._map)
		self._menu = EditorMenu(self._engine, self)
		self._submodules = (self._map, self._minimap, self._tiles, self._menu, self._cursor)
		self._refresh = True

	def show(self):
		"""Wyświetla edytor poziomów."""

		try:
			while self._engine.tick():
				self.events = self._engine.events()
				for event in self.events:
					if event.type == QUIT:
						raise engine.EngineQuit()

					if event.type == KEYUP and event.key == K_ESCAPE:
						self._engine.previousModule()
						raise EditorQuit()

					if event.type in (MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP):
						if event.type == MOUSEBUTTONDOWN and event.button in (4, 5): # zmiana poziomów kółkiem myszy, dodawanie w razie potrzeby
							_step = 0
							if event.button == 4:
								if self._map.getStorey() == 0 and len(self._level) < LEVEL_LIMIT:
									self._level.insert(0, [[Field((x, y)) for x in xrange(MAP_SIZE)] for y in xrange(MAP_SIZE)])
									self._map.updateLevel(self._level)
									_step += 1

								else:
									if self._map.getStorey() + 1 == self._map.getStoreys() and utils.emptyStorey(self._level[-1]):
										del self._level[-1]
										self._map.updateLevel(self._level)

									while len(self._level) > 1 and utils.emptyStorey(self._level[0]):
										del self._level[0]
										self._map.updateLevel(self._level)
										_step -= 1

							elif event.button == 5:
								if self._map.getStorey() + 1 == self._map.getStoreys() and len(self._level) < LEVEL_LIMIT:
									self._level.append([[Field((x, y)) for x in xrange(MAP_SIZE)] for y in xrange(MAP_SIZE)])
									self._map.updateLevel(self._level)

								else:
									if self._map.getStorey() == 0 and utils.emptyStorey(self._level[0]):
										del self._level[0]
										self._map.updateLevel(self._level)
										_step -= 1

									while len(self._level) > 1 and utils.emptyStorey(self._level[-1]):
										del self._level[-1]
										self._map.updateLevel(self._level)

							self._map.switchStorey(_step + (event.button == 4 and -1 or 1))

						for submodule in self._submodules:
							if submodule.getRectangle().collidepoint(event.pos):
								x, y, _, _ = submodule.getRectangle()
								_pos = event.pos[0] - x, event.pos[1] - y

							else:
								_pos = None

							submodule.mouseEvent(event, _pos)

				self.surface = self._background.copy()
				updated = []
				for submodule in (self._map, self._minimap, self._tiles, self._menu, self._cursor):
					updated.extend(submodule.update())
					submodule.draw(self.surface)

				if self._refresh:
					self._engine.show(self.surface)
					self._refresh = False

				else:
					self._engine.show(self.surface, updated)

		except EditorQuit:
			pass

class EditorQuit(Exception):
	"""Wyjście z edytora."""

	pass

class EditorButton(MenuButton):
	"""Przycisk Edytora w menu."""

	def __init__(self, _engine):
		super(EditorButton, self).__init__(_engine, 'Edytor')

	def callback(self):
		"""Włączanie edytora."""

		self._engine.addModule(Editor(self._engine))
		self._engine.activateModule('Editor')
		raise MenuQuit()

class EditorMenu(object):
	"""Mini-menu w edytorze."""

	def __init__(self, _engine, _editor):
		super(EditorMenu, self).__init__()
		self.images = {
			'save': utils.loadImage('data/gfx/save.png', alpha = True),
			'cancel': utils.loadImage('data/gfx/cancel.png', alpha = True),
		}

		self._engine = _engine
		self._editor = _editor
		self.screenUpdated()
		self.surface = pygame.Surface((192, 32))
		self.surface.fill((1, 5, 4))
		self.surface.set_colorkey((1, 5, 4))
		self._save = pygame.Rect(60, 0, 32, 32)
		self.surface.blit(self.images['save'], self._save)
		self._clear = pygame.Rect(100, 0, 32, 32)
		self.surface.blit(self.images['cancel'], self._clear)

	def getRectangle(self):
		"""Zwraca obszar zajmowany przez menu."""

		return pygame.Rect(self._pos[0], self._pos[1], 192, 32)

	def screenUpdated(self):
		"""Aktualizuje pozycję menu i wymusza odświeżenie obszaru."""

		self._resx, self._resy = self._engine.getResolution()
		_resx = self._resx
		self._resx = int((self._resx - 200) / 32) * 32
		_pad = (_resx - self._resx - 192) / 2
		self._pos = (self._resx + _pad, 2 * _pad + 470)
		self._refresh = True

	def update(self):
		if self._refresh:
			self._refresh = False
			return [(self._pos[0], self._pos[1], 192, 32)]

		return []

	def draw(self, surface):
		"""Rysuje menu na powierzchni."""

		surface.blit(self.surface, (self._pos[0], self._pos[1]))

	def mouseEvent(self, _event, _pos = None):
		"""Obsługa zdarzeń myszy."""

		if not _pos:
			return

		if _event.type == MOUSEBUTTONDOWN and _event.button == 1:
			if self._save.collidepoint(_pos):
				self._editor.saveLevel()

			elif self._clear.collidepoint(_pos):
				self._editor.clearLevel()
