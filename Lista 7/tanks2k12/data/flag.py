# -*- encoding: utf8 -*-

import sys
import random
import pygame
from pygame.locals import *
from utils import *

CATCH_RANGE = 32

class Flag(AnimatedSprite):
	images = None
	def __init__(self, _engine, _map, _player, _pos):
		super(Flag, self).__init__(_pos)
		if not Flag.images:
			Flag.images = loadImages('data/gfx/flag/', alpha = True)

		self._engine = _engine
		self._map = _map
		self._start = tuple(_pos)
		self._player = self._engine.players[_player]
		self._tank = None
		self._detached = False

		self.image = self.images[str(_player)]['0']
		self.rect = self.image.get_rect()
		self.rect.centerx, self.rect.centery = self._pos
		self.radius = CATCH_RANGE
		self.i = 0

	def getColor(self):
		return self._player['color']

	def update(self):
		if not self._detached:
			gather = list(filter(lambda tank: tank.getPlayerID() == self._player['id'] ^ 1, pygame.sprite.spritecollide(self, self._map.tanks, False, pygame.sprite.collide_circle)))
			if gather:
				random.shuffle(gather)
				self._detached = True
				self._tank = gather[0]
				self._tank.flagged = True

		else:
			gather = pygame.sprite.spritecollide(self, self._map.flags, False, pygame.sprite.collide_circle)
			if len(gather) > 1:
				self._engine.players[self._player['id'] ^ 1]['score'] += 1
				self._detached = False
				self._tank.flagged = False
				self._tank = None

			else:
				self._pos = self._tank.getPos()
				self._pos = (self._pos[0] + 8, self._pos[1] - 20)
				self.rect.centerx, self.rect.centery = self._pos
				if not self._tank.health:
					self._detached = False
					self._tank = None


		if not self._detached:
			self.rect.centerx, self.rect.centery = self._pos = self._start

		self.i += 1
		self.i %= 2
		if self.i % 2 == 0:
			self.nextFrame(self.images[str(self._player['id'])])

		if self._detached:
			self.image.set_alpha(128)

