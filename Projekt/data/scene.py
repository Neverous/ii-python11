# -*- encoding: utf8 -*-
# Maciej Szeptuch 2012

import time
import pygame
import engine
import utils
from pygame.locals import *
from menu import MenuButton, MenuQuit
from map import Map, HoverLayer, MapLayer
from minimap import Minimap
from cursor import Cursor
from inventory import Inventory
from chestitems import ChestItems
import field

# CREATURES
import hero
from mage import Mage
from troll import Troll
from skeleton import Skeleton
from spider import Spider
# ITEMS
from arrows import Arrows
from sword import Sword
from axe import Axe
from armor import Armor
from bow import Bow
from potion import ManaPotion, LifePotion
from shield import Shield

AVAILABLE_ITEMS = (Arrows, Arrows, Sword, Axe, Armor, Bow, Shield, ManaPotion, LifePotion) # arrows x2 żeby wypadały trochę częściej

class Scene(engine.Module):
	"""Główny ekran gry."""

	def __init__(self, _engine):
		super(Scene, self).__init__(_engine)
		self.side = utils.loadImage('data/gfx/side.png')
		self._background = pygame.Surface((self._resx, self._resy))
		self._background.blit(self.side, (self._resx - 232, self._resy - 1500))
		self.surface = self._background.copy()
		self._actual = []
		self._level = utils.loadLevel('data/level.dat')
		self._map = Map(_engine, self, self._level)
		self._minimap = Minimap(_engine, self._map)
		self._cursor = Cursor(_engine, self._map)
		self._creatureLayer = CreatureLayer(self._map, self._cursor) # Warstwa potworów
		self._map.addLayer('Creatures', 2, self._creatureLayer)
		self._map.addLayer('Missiles', 3, MissilesLayer(self._map)) # Warstwa pocisków(strzał, kuli ognia itp.)
		self._shadow = ShadowLayer(self._map)
		self._map.addLayer('Shadow', 5, self._shadow) # Mgła wojny
		self._monsters = []
		self._freeobjects = pygame.sprite.Group() # Wolne obiekty na scenie
		_counter = 0
		_start = 0
		# szukanie bohatera w lochu
		for l, storey in enumerate(self._level):
			for row in storey:
				for cell in row:
					if cell.getModifier() & field.MODIFIER_HERO:
						self._hero = hero.Hero(self._map, cell.getGrid() + (l,))
						self._hero.move((0, 0, 0))
						self._map.switchStorey(l)
						_start = l
						self._creatureLayer.add('hero', self._hero.getSprite(self._creatureLayer, 'hero'))
						break

		# szukanie potworów
		for l, storey in enumerate(self._level):
			for row in storey:
				for cell in row:
					if cell.getModifier() & field.MODIFIER_SPIDER:
						_monster = Spider(self._map, cell.getGrid() + (l,))
						self._monsters.append(('spider', _monster))
						if l == _start:
							self._creatureLayer.add('spider_' + str(_counter), _monster.getSprite(self._creatureLayer, 'spider_' + str(_counter)))
							self._actual.append(('spider_' + str(_counter), _monster))
							_monster.move((0, 0, 0))
							_counter += 1

					elif cell.getModifier() & field.MODIFIER_SKELETON:
						_monster = Skeleton(self._map, cell.getGrid() + (l,))
						self._monsters.append(('skeleton', _monster))
						if l == _start:
							self._creatureLayer.add('skeleton_' + str(_counter), _monster.getSprite(self._creatureLayer, 'skeleton_' + str(_counter)))
							self._actual.append(('skeleton_' + str(_counter), _monster))
							_monster.move((0, 0, 0))
							_counter += 1

					elif cell.getModifier() & field.MODIFIER_MAGE:
						_monster = Mage(self._map, cell.getGrid() + (l,))
						self._monsters.append(('mage', _monster))
						if l == _start:
							self._creatureLayer.add('mage_' + str(_counter), _monster.getSprite(self._creatureLayer, 'mage_' + str(_counter)))
							self._actual.append(('mage_' + str(_counter), _monster))
							_monster.move((0, 0, 0))
							_counter += 1

					elif cell.getModifier() & field.MODIFIER_TROLL:
						_monster = Troll(self._map, cell.getGrid() + (l,))
						self._monsters.append(('troll', _monster))
						if l == _start:
							self._creatureLayer.add('troll_' + str(_counter), _monster.getSprite(self._creatureLayer, 'troll_' + str(_counter)))
							self._actual.append(('troll_' + str(_counter), _monster))
							_monster.move((0, 0, 0))
							_counter += 1

		if not self._hero:
			raise Exception('Brak bohatera w lochu!?')

		self._statusbar = StatusBar(_engine, self._hero) # pasek życia/many itp. / statusu
		self.inventory = Inventory(_engine, self._hero, self._hero.inventory, self._freeobjects)
		self.chestitems = ChestItems(_engine, self._hero, self._freeobjects)
		self._submodules = (self._map, self._minimap, self._statusbar, self.inventory, self.chestitems, self._cursor)
		self._play = True
		self._refresh = True

	def isPlaying(self):
		"""Czy gracz nadal gra?"""

		return self._play

	def screenUpdated(self):
		"""Aktualizuje obrazy tła i submoduły."""

		super(Scene, self).screenUpdated()
		self._refresh = True
		self._background = pygame.Surface((self._resx, self._resy))
		self._background.blit(self.side, (self._resx - 232, self._resy - 1500))
		self.surface = pygame.transform.smoothscale(self.surface, (self._resx, self._resy))
		for submodule in self._submodules:
			submodule.screenUpdated()

	def show(self):
		if not self._play:
			self._engine.previousModule()
			return

		try:
			while self._engine.tick():
				for event in self._engine.events():
					if event.type == QUIT:
						raise engine.EngineQuit()

					if event.type == KEYDOWN:
						if event.key == K_ESCAPE:
							self._engine.previousModule()
							raise SceneQuit()

						elif event.key in hero.MAGIC_KEYS:
							self._hero.setSpell(hero.KEY_MAP[event.key])

					if event.type in (MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP):
						for submodule in self._submodules:
							if submodule.getRectangle().collidepoint(event.pos):
								x, y, _, _ = submodule.getRectangle()
								_pos = event.pos[0] - x, event.pos[1] - y

							else:
								_pos = None

							submodule.mouseEvent(event, _pos)
							if submodule == self._map and event.type == MOUSEBUTTONDOWN and _pos: # obsługa otwierania skrzynki(głównie)
								_field = self._map.getLayer('Fields').get(_pos, True)
								if _field:
									_field.getLogic().clicked(self, self._hero)

							if submodule == self._map and event.type == MOUSEBUTTONUP and event.button == 1 and _pos: # upuszczanie przedmiotu
								_field = self._map.getLayer('Fields').get(_pos, True)
								if _field:
									_field = _field.getLogic()

								if _field and utils.distance(_field.getGrid()[:2], self._hero.getGrid()[:2]) <= 1:
									for _obj in self._freeobjects:
										if not _obj.attach(_field):
											_obj.attach(_obj.getAttached())
								else:
									for _obj in self._freeobjects:
										_obj.attach(_obj.getAttached())

							if submodule == self.inventory and event.type == MOUSEBUTTONUP and event.button == 1 and _pos: # ↑
								for _obj in self._freeobjects:
									if not _obj.attach(self.inventory.getCell(_pos)):
										_obj.attach(_obj.getAttached())

							if submodule == self.chestitems and event.type == MOUSEBUTTONUP and event.button == 1 and _pos: # ↑
								for _obj in self._freeobjects:
									if not self.chestitems.opened or not _obj.attach(self.chestitems.getCell(_pos)):
										_obj.attach(_obj.getAttached())

						for _obj in self._freeobjects:
							_obj.mouseEvent(event)

						if event.type == MOUSEBUTTONDOWN and event.button == 3 and self._map.getRectangle().collidepoint(event.pos): # rzucanie czaru
							self._hero.castSpell()

						if event.type == MOUSEBUTTONDOWN and event.button == 1 and self._map.getRectangle().collidepoint(event.pos): # atak
							self._hero.punch()

				if self._hero.getGrid()[2] != self._map.getStorey(): # zmiana poziomu lochu
					self._map.removeLayer('Missiles')
					self._map.addLayer('Missiles', 3, MissilesLayer(self._map))
					self._map.switchStorey(self._hero.getGrid()[2] - self._map.getStorey())
					self._shadow.clear()
					for _id, _ in self._actual:
						self._creatureLayer.remove(_id)

					self._actual = []
					_counter = 0
					_storey = self._map.getStorey()
					for _name, _monster in self._monsters:
						if _monster.getGrid()[2] == _storey:
							self._creatureLayer.add(_name + '_' + str(_counter), _monster.getSprite(self._creatureLayer, _name + '_' + str(_counter)))
							self._actual.append((_name + '_' + str(_counter), _monster))
							_monster.move((0, 0, 0))
							_counter += 1

				else:
					for key in hero.DIRECTION_KEYS:
						if pygame.key.get_pressed()[key]:
							self._hero.move(hero.KEY_MAP[key])

				if self._hero.getDestination(): # przesuwanie mapy za bohaterem
					x, y = self._hero.getPos()
					_, _, w, h = self._map.getRectangle()
					self._map.setShift((w / 2 - x, h / 2 - y))

				if not self._hero.getLife(): # przegrana
					utils.drawText(self.surface, "Game Over", 40, (255, 255, 255), (self._resx / 2, self._resy / 2))
					self._play = False
					self._engine.show(self.surface)
					time.sleep(3)
					self._engine.previousModule()
					raise SceneQuit()

				if not self._monsters: # wygrana
					utils.drawText(self.surface, "Win", 50, (255, 255, 255), (self._resx / 2, self._resy / 2))
					self._play = False
					self._engine.show(self.surface)
					time.sleep(3)
					self._engine.previousModule()
					raise SceneQuit()

				_hero = self._hero.getPos()
				_shift = self._map.getShift()
				_hero = _hero[0] + _shift[0], _hero[1] + _shift[1]
				_mouse = pygame.mouse.get_pos()
				_mouse = _mouse[0] - _hero[0], _mouse[1] - _hero[1]
				_angle = utils.vectorAngle((0, 1), _mouse)
				if -45 <= _angle < 45:
					self._hero.setDirection('s')

				elif -135 <= _angle < -45:
					self._hero.setDirection('e')

				elif 45 <= _angle < 135:
					self._hero.setDirection('w')

				else:
					self._hero.setDirection('n')

				self._shadow.reveal(self._hero.getPos())
				self.surface = self._background.copy()
				updated = []
				for submodule in self._submodules:
					updated.extend(submodule.update())
					submodule.draw(self.surface)

				for _obj in self._freeobjects:
					updated.extend(_obj.update())
					_obj.draw(self.surface)

				if self._refresh:
					self._engine.show(self.surface)
					self._refresh = False

				else:
					self._engine.show(self.surface, updated)

				_actual = []
				for _id, _monster in self._actual:
					if _monster.getGrid()[2] != self._map.getStorey():
						self._creatureLayer.remove(_id)

					else:
						_actual.append((_id, _monster))

				self._actual = _actual
				for _id, _monster in self._monsters: # umierające potwory dodają exp bohaterowi
					if not _monster.getLife():
						self._monsters.remove((_id, _monster))
						self._hero.addExperience(_monster.stats['experience'])

		except SceneQuit:
			pass

class ShadowLayer(MapLayer):
	"""Mgła wojny. Tylko jeden punkt jest odkryty na raz."""

	def __init__(self, _map):
		super(ShadowLayer, self).__init__(_map)
		self.clear()
		self._last = ((0, 0), 0)

	def mouseEvent(self, _event, _pos = None):
		"""Blokuje zdarzenia na polach których nie widać."""

		if not _pos:
			return True

		if not utils.distance(self._last[0], _pos) <= self._last[1]:
			return False

		return True

	def clear(self):
		"""Zaciemnia całą warstwę."""

		self.surface.fill((0, 0, 0, 245))
		self._check = True

	def reveal(self, _pos, _radius = 104):
		"""Odkrywa kawałek mapy."""

		if self._last:
			if self._last == (_pos, _radius):
				return

			pygame.draw.circle(self.surface, (0, 0, 0, 192), map(int, self._last[0]), self._last[1])
			self._updated.append((self._last[0][0] - self._last[1], self._last[0][1] - self._last[1], 2 * self._last[1], 2 * self._last[1]))

		self._last = (_pos, _radius)
		for _rad in xrange(_radius, 0, -1):
			pygame.draw.circle(self.surface, (0, 0, 0, _rad * 192 / _radius), map(int, _pos), _rad)

		self._updated.append((_pos[0] - _radius, _pos[1] - _radius, 2 * _radius, 2 * _radius))
		self._check = True

	def getRevealed(self):
		"""Zwraca aktualnie odkryty obszar."""

		return self._last

class CreatureLayer(HoverLayer):
	"""Warstwa ze stworami."""

	def __init__(self, _map, _cursor):
		super(CreatureLayer, self).__init__(_map)
		self._cursor = _cursor

	def mouseEvent(self, _event, _pos = None):
		"""Ustawia kursor na atak jeśli nad potworem."""

		self._cursor.setCursor()
		if not _pos:
			return True

		for _sprite in self._sprites:
			if _sprite.rect.collidepoint(_pos):
				self._cursor.setCursor('attack')

		return True

	def update(self):
		"""Rysuj tylko to co nie jest zasłonięte przez mgłę."""

		if self._refresh:
			self._refresh = False
			return [(0, 0) + self.surface.get_size()]

		updated = list(self._updated)
		self._updated = []
		_shadow = self._map.getLayer('Shadow')
		if _shadow:
			_shadow = _shadow.getRevealed()

		for field in self._sprites:
			_upd = field.update()
			if _shadow and utils.distance(field.getPos(), _shadow[0]) > _shadow[1]:
				continue

			if _upd:
				updated.extend(_upd)
				field.draw(self.surface)

		if updated:
			self._check = True

		return updated

class MissilesLayer(HoverLayer):
	"""Warstwa z efektami ataków (ogień, strzały, itp.)."""

	def update(self):
		"""Rysuj tylko to co nie jest zasłonięte przez mgłę."""

		if self._refresh:
			self._refresh = False
			return [(0, 0) + self.surface.get_size()]

		updated = list(self._updated)
		self._updated = []
		_shadow = self._map.getLayer('Shadow')
		if _shadow:
			_shadow = _shadow.getRevealed()

		for field in self._sprites:
			_upd = field.update()
			if _shadow and utils.distance(field.getPos(), _shadow[0]) > _shadow[1]:
				continue

			if _upd:
				updated.extend(_upd)
				field.draw(self.surface)

		if updated:
			self._check = True

		return updated

class SceneQuit(Exception):
	"""Wyjście z ekranu gry."""

	pass

class NewGameButton(MenuButton):
	"""Przycisk nowej gry."""

	def __init__(self, _engine):
		super(NewGameButton, self).__init__(_engine, 'Nowa gra')

	def update(self):
		"""Zmiana napisu z kontynuuj na Nowa gra."""

		_scene = self._engine.getModule('Scene')
		if not _scene:
			return

		if self.text == 'Nowa gra' and _scene.isPlaying():
			self.text = 'Kontynuuj'

		elif self.text == 'Kontynuuj' and not _scene.isPlaying():
			self.text = 'Nowa gra'

	def callback(self):
		"""Rozpoczynanie nowej gry."""

		_scene = self._engine.getModule('Scene')
		if not _scene or not _scene.isPlaying():
			self._engine.addModule(Scene(self._engine))

		self._engine.activateModule('Scene')
		raise MenuQuit()

class StatusBar(object):
	def __init__(self, _engine, _hero):
		super(StatusBar, self).__init__()
		self._engine = _engine
		self._hero = _hero
		self.screenUpdated()
		self.images = {
			'background': utils.loadImage('data/gfx/healthmanabar.png', alpha = True),
			'mask': utils.loadImage('data/gfx/healthmanamask.png', alpha = True),
			'fireon': utils.loadImage('data/gfx/fireon.png', alpha = True),
			'fireoff': utils.loadImage('data/gfx/fireoff.png', alpha = True),
			'iceon': utils.loadImage('data/gfx/iceon.png', alpha = True),
			'iceoff': utils.loadImage('data/gfx/iceoff.png', alpha = True),
			'healon': utils.loadImage('data/gfx/healon.png', alpha = True),
			'healoff': utils.loadImage('data/gfx/healoff.png', alpha = True),
		}

		self._before = ((0, 0, 0), (0, 0, 0))
		self._life = (0, 0)
		self._mana = (0, 0)
		self._spell = None

	def screenUpdated(self):
		"""Aktualizuje pozycję i wymusza odświeżenie obszaru."""

		self._resx, self._resy = self._engine.getResolution()
		_resx = self._resx
		self._resx = int((self._resx - 200) / 32) * 32
		_pad = (_resx - self._resx - 192) / 2
		self._pos = (self._resx + _pad, _pad + 192)
		self._refresh = True

	def getRectangle(self):
		"""Zwraca obszar zajmowany przez menu."""

		return pygame.Rect(self._pos[0], self._pos[1], 192, 16)

	def mouseEvent(self, _event, _pos):
		"""Obsługa zdarzeń myszy."""

		pass

	def update(self):
		if self._refresh:
			self._refresh = False
			return [tuple(self.getRectangle())]

		_refresh = False
		_life = (self._hero.getLife(True), self._hero.getLife(), self._hero.stats['maxlife'])
		_mana = (self._hero.getMana(True), self._hero.getMana(), self._hero.stats['maxmana'])
		if self._before != (_life, _mana):
			self._before = (_life, _mana)
			_refresh = True

		_spell = self._hero.getSpell()
		if _spell != self._spell:
			_refresh = True
			self._spell = _spell

		if _refresh:
			return [tuple(self.getRectangle())]

		return []

	def draw(self, surface):
		"""Rysuje minimapę na powierzchni."""

		surface.blit(self.images['background'], self._pos)
		pygame.draw.rect(surface, (0, 255, 0), (self._pos[0] + 2, self._pos[1] + 1, max(0, int(62 * self._before[0][0])), 14))
		utils.drawText(surface, "%d/%d" % self._before[0][1:3], 10, (0, 0, 0), (self._pos[0] + 32, self._pos[1] + 8))
		pygame.draw.rect(surface, (0, 0, 255), (self._pos[0] + 66, self._pos[1], max(0, int(62 * self._before[1][0])), 14))
		utils.drawText(surface, "%d/%d" % self._before[1][1:3], 10, (0, 0, 0), (self._pos[0] + 96, self._pos[1] + 8))
		surface.blit(self.images['mask'], self._pos)

		surface.blit(self.images['fire' + (self._spell == hero.MAGIC_FIRE and 'on' or 'off')], (self._pos[0] + 136, self._pos[1]))
		utils.drawText(surface, "1", 10, (0, 0, 0), (self._pos[0] + 144, self._pos[1] + 8))

		surface.blit(self.images['ice' + (self._spell == hero.MAGIC_ICE and 'on' or 'off')], (self._pos[0] + 152, self._pos[1]))
		utils.drawText(surface, "2", 10, (0, 0, 0), (self._pos[0] + 160, self._pos[1] + 8))

		surface.blit(self.images['heal' + (self._spell == hero.MAGIC_HEAL and 'on' or 'off')], (self._pos[0] + 168, self._pos[1]))
		utils.drawText(surface, "3", 10, (0, 0, 0), (self._pos[0] + 176, self._pos[1] + 8))
