# -*- encoding: utf8 -*-

import time
import random
import pygame
from pygame.locals import *
from utils import *
from tank import Tank
from flag import Flag
from workshop import Workshop

FIELD_BLOCKED   = 1
FIELD_SLOW      = 2
FIELD_FLAG1     = 4
FIELD_FLAG2     = 8
FIELD_SPAWN1    = 16
FIELD_SPAWN2    = 32
FIELD_WORKSHOP1 = 64
FIELD_WORKSHOP2 = 128

DIRECTION_NONE = 1
DIRECTION_UP = 2
DIRECTION_RIGHT = 4
DIRECTION_DOWN = 8
DIRECTION_LEFT = 16

SLIDE_SPEED = 15

TANKS = 10

class Map(object):
	tiles = None
	def __init__(self, _engine):
		super(Map, self).__init__()
		if not Map.tiles:
			Map.tiles = loadImages('data/gfx/tiles/', alpha = True)

		self._engine = _engine
		self._level = self._engine.getLevel()
		self._above = []
		self._workshops = pygame.sprite.Group()
		self.flags = pygame.sprite.Group()
		self.tanks = pygame.sprite.Group()
		self.explosions = pygame.sprite.Group()
		self.missiles = pygame.sprite.Group()
		self._holdpos = (False, False)
		self._pos = [0, 0]
		self._w, self._h = len(self._level[0]), len(self._level)
		self._mw, self._mh = self._w * 32, self._h * 32
		self._background = pygame.Surface((self._mw, self._mh))
		self._debugbackground = pygame.Surface((self._mw, self._mh))
		self._debugbackground.fill((1, 5, 4))
		self._debugbackground.set_colorkey((1, 5, 4))
		self._debugbackground.set_alpha(96)
		self.debug = pygame.Surface((self._mw, self._mh))
		self.debug.fill((1, 5, 4))
		self.debug.set_alpha(96)
		self.debug.set_colorkey((1, 5, 4))
		self.screenUpdated()
		spawn1, spawn2 = None, None
		for r, row in enumerate(self._level):
			for c, (cell, mask) in enumerate(row):
				_, _, x, y = self.tiles[str(cell)].get_rect()
				self._background.blit(self.tiles[str(cell)], ((c + 1) * 32 - x, (r + 1) * 32 - y))
				pygame.draw.rect(self._debugbackground, (0, 0, 0), (c * 32, r * 32, 32, 32), 1)
				if mask & FIELD_SPAWN1:
					self._engine.players[0]['spawn'] = spawn1 = (c, r)
					
				if mask & FIELD_SPAWN2:
					self._engine.players[1]['spawn'] = spawn2 = (c, r)

				if mask & FIELD_FLAG1:
					self._engine.players[0]['flag'] = flag = Flag(_engine, self, 0, (c * 32 + 16, r * 32 + 16))
					self.flags.add(flag)

				if mask & FIELD_FLAG2:
					self._engine.players[1]['flag'] = flag = Flag(_engine, self, 1, (c * 32 + 16, r * 32 + 16))
					self.flags.add(flag)

				if mask & FIELD_WORKSHOP1:
					self._engine.players[0]['workshop'] = workshop = Workshop((c * 32 + 16, r * 32 + 16))
					self._workshops.add(workshop)

				if mask & FIELD_WORKSHOP2:
					self._engine.players[1]['workshop'] = workshop = Workshop((c * 32 + 16, r * 32 + 16))
					self._workshops.add(workshop)

				if str(cell) + 'a' in self.tiles:
					self._above.append((str(cell) + 'a', ((c + 1) * 32 - x, (r + 1) * 32 - y)))

		spawn1 = neighbours(spawn1, lambda (x, y): not self.getGridField((x, y))[1] & FIELD_BLOCKED, TANKS)
		spawn2 = neighbours(spawn2, lambda (x, y): not self.getGridField((x, y))[1] & FIELD_BLOCKED, TANKS)
		random.shuffle(spawn1)
		random.shuffle(spawn2)
		
		for t in xrange(TANKS):
			x, y = spawn1[t]
			_engine.players[0]['tanks'].append(Tank(_engine, self, 0, (x * 32 + 16, y * 32 + 16)))

		for t in xrange(TANKS):
			x, y = spawn2[t]
			_engine.players[1]['tanks'].append(Tank(_engine, self, 1, (x * 32 + 16, y * 32 + 16)))

		self.tanks.add(_engine.players[0]['tanks'])
		self.tanks.add(_engine.players[1]['tanks'])
		self.surface = self._background.copy()

	def getPos(self):
		return self._pos

	def getGridMasks(self):
		return tuple([tuple(map(lambda f: f[1], row)) for row in self._level])

	def getPointField(self, (x, y)):
		if 0 <= x < self._mw and 0 <= y < self._mh:
			return self._level[int(y / 32)][int(x / 32)]

		return (0, FIELD_BLOCKED)

	def getGridField(self, (x, y)):
		if 0 <= x < self._w and 0 <= y < self._h:
			return self._level[y][x]

		return (0, FIELD_BLOCKED)

	def getSize(self):
		return (self._mw, self._mh)
		
	def update(self):
		self.surface = self._background.copy()
		toRemove = []
		for tank in self.tanks:
			if not tank.health:
				toRemove.append(tank)

		self.tanks.remove(toRemove)
		for tank in toRemove:
			try: self._engine.players[0]['tanks'].remove(tank)
			except ValueError: pass

			try: self._engine.players[1]['tanks'].remove(tank)
			except ValueError: pass

		toRemove = []
		for explosion in self.explosions:
			if not explosion.health:
				toRemove.append(explosion)

		self.explosions.remove(toRemove)
		toRemove = []
		for missile in self.missiles:
			if not missile.health:
				toRemove.append(missile)

		self.missiles.remove(toRemove)
		self.missiles.update()
		self.explosions.update()
		self.tanks.update()
		self.flags.update()
		self._workshops.update()
		self.tanks.draw(self.surface)
		self.flags.draw(self.surface)
		self.missiles.draw(self.surface)
		for tile, pos in self._above:
			self.surface.blit(self.tiles[tile], pos)

		self.explosions.draw(self.surface)

	def screenUpdated(self):
		self._resx, self._resy = self._engine.getResolution()
		self._holdpos = [False, False]
		if self._resx > self._mw:
			self._holdpos[0] = True
			self._pos[0] = (self._resx - self._mw) / 2

		if self._resy > self._mh:
			self._holdpos[1] = True
			self._pos[1] = (self._resy - self._mh) / 2

		self._holdpos = tuple(self._holdpos)

	def move(self, direction):
		if not self._holdpos[0]:
			if direction & DIRECTION_LEFT:
				self._pos[0] += SLIDE_SPEED

			elif direction & DIRECTION_RIGHT:
				self._pos[0] -= SLIDE_SPEED

			self._pos[0] = max(min(0, self._pos[0]), -self._mw + self._resx)

		if not self._holdpos[1]:
			if direction & DIRECTION_UP:
				self._pos[1] += SLIDE_SPEED

			elif direction & DIRECTION_DOWN:
				self._pos[1] -= SLIDE_SPEED

			self._pos[1] = max(min(0, self._pos[1]), -self._mh + self._resy)

	def draw(self, surface):
		surface.blit(self.surface, self._pos)
		if self._engine.options['debug']:
			surface.blit(self._debugbackground, self._pos)
			surface.blit(self.debug, self._pos)
			self.debug = pygame.Surface((self._mw, self._mh))
			self.debug.set_alpha(96)
			self.debug.fill((1, 5, 4))
			self.debug.set_colorkey((1, 5, 4))
