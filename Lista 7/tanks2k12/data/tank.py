# -*- encoding: utf8 -*-

import math
import pygame
from pygame.locals import *
from utils import *
import map
from missile import Missile
from shot import Shot

MAX_SPEED = 3.0
SLOW_FACTOR = 4
MAX_MISSILES = 20
MAX_HEALTH = 400

class Tank(pygame.sprite.Sprite):
	images = None
	def __init__(self, _engine, _map, _player, _pos):
		super(Tank, self).__init__()
		if not Tank.images:
			Tank.images = loadImages('data/gfx/tank/', alpha = True)
			Tank.images['focus'] = loadImage('data/gfx/focus.png', alpha = True)

		self._engine = _engine
		self._map = _map
		self._player = _engine.players[_player]
		self._pos = list(_pos)
		self._playerWorkshop = _player and map.FIELD_WORKSHOP2 or map.FIELD_WORKSHOP1
		self._opponentWorkshop = _player and map.FIELD_WORKSHOP1 or map.FIELD_WORKSHOP2
		
		self.focus = False
		self.flagged = False
		self.repair = False
		self.missiles = MAX_MISSILES
		self.health = MAX_HEALTH
		self.tracks = 0
		self.barrel = 0
		self._color = list(self._player['color'])
		self._speed = 0
		self._vx, self._vy = angleVector(2.0 * math.pi * self.tracks / 32)
		self._reload = 0
		self.updateImage()
		self.rect = self.image.get_rect()
		self.rect.centerx, self.rect.centery = _pos

	def setFocus(self, focus):
		self.focus = focus
		self.updateImage()

	def getPos(self):
		return tuple(self._pos)

	def getSpeed(self):
		return self._speed

	def getPlayerID(self):
		return self._player['id']

	def updateImage(self):
		self.image = Tank.images['tracks'][str(self.tracks)].copy()
		self.mask = pygame.mask.from_surface(self.image)
		self.image.blit(Tank.images['barrel'][str(self.barrel)], (0, 0))
		pygame.draw.rect(self.image, (0, 0, 0, 128), (1, 1, 30, 4))
		pygame.draw.rect(self.image, self._color + [128], (2, 2, 28 * self.health / MAX_HEALTH, 2))
		if not self._player['id']:
			drawText(self.image, str(self.missiles), 8, (255, 255, 255, 128), (26, 9))

		if self.focus:
			self.image.blit(self.images['focus'], (0, 0))

	def accelerate(self):
		self._speed = min(self._speed + 1, MAX_SPEED)

	def fullaccelerate(self):
		self._speed = MAX_SPEED

	def reverse(self):
		self._speed = max(self._speed - 1, -MAX_SPEED)

	def fullreverse(self):
		self._speed = -MAX_SPEED

	def decelerate(self):
		if self._speed > 0:
			self._speed = max(self._speed - 0.5, 0)

		elif self._speed < 0:
			self._speed = min(self._speed + 0.5, 0)

	def turnLeft(self):
		self.tracks = (self.tracks - 1) % 32
		self._vx, self._vy = angleVector(2.0 * math.pi * self.tracks / 32)
		self.barrelLeft()
		
	def turnRight(self):
		self.tracks = (self.tracks + 1) % 32
		self._vx, self._vy = angleVector(2.0 * math.pi * self.tracks / 32)
		self.barrelRight()

	def barrelLeft(self):
		self.barrel = (self.barrel - 1) % 32

	def barrelRight(self):
		self.barrel = (self.barrel + 1) % 32

	def move(self):
		if not self._speed:
			return True

		moved = True
		speed = 1.0 * self._speed
		if self._map.getPointField(self._pos)[1] & map.FIELD_SLOW:
			speed /= SLOW_FACTOR
		
		_before = tuple(self._pos)
		collidebefore = filter(lambda t: t != self, pygame.sprite.spritecollide(self, self._map.tanks, False, pygame.sprite.collide_mask))
		vx = speed * self._vx
		vy = speed * self._vy
		self._pos[0] += vx
		self._pos[1] += vy
		self.rect.centerx, self.rect.centery = self._pos
		flag = self._map.getPointField(self._pos)[1]
		collide = filter(lambda t: t != self, pygame.sprite.spritecollide(self, self._map.tanks, False, pygame.sprite.collide_mask))
		if len(collide):
			if len(collidebefore) and distance(self._pos, collide[0].getPos()) < distance(_before, collidebefore[0].getPos()):
				self._pos[0] -= vx
				self._pos[1] -= vy
				self._speed = 0
				moved = False

		elif flag & map.FIELD_BLOCKED or flag & self._opponentWorkshop:
			self._pos[0] -= vx * 1.1
			self._pos[1] -= vy * 1.1
			self._speed = 0
			moved = False

		elif flag & self._playerWorkshop:
			if self._player['workshop'].occupied and self._player['workshop'].occupied != self:
				self._pos[0] -= vx
				self._pos[1] -= vy
				self._speed = 0
				moved = False

			elif distance(self._player['workshop'].getPos(), self.getPos()) < 16:
				self._player['workshop'].occupied = self
				self.repair = True

		self.rect.centerx, self.rect.centery = self._pos
		return moved

	def shoot(self):
		if self.repair:
			return

		if not self._reload and self.missiles:
			vx, vy = angleVector(2.0 * math.pi * self.barrel / 32)
			pos = list(self._pos)
			pos[0] += 20 * vx
			pos[1] += 20 * vy
			self._map.explosions.add(Shot(pos))
			self._map.missiles.add(Missile(self._engine, self._map, self, pos, (vx, vy)))
			self._reload = 40
			self.missiles -= 1
			self.updateImage()

	def hit(self, points):
		if self.repair:
			return

		self.health = max(0, self.health - points)
		self.updateImage()

	def update(self):
		self._reload = max(self._reload - 1, 0)
		if self.focus:
			key = pygame.key.get_pressed()
			changed = False
			if key[K_a]:
				self.turnLeft()
				changed = True

			elif key[K_d]:
				self.turnRight()
				changed = True

			if key[K_q]:
				self.barrelLeft()
				changed = True

			elif key[K_e]:
				self.barrelRight()
				changed = True

			if key[K_w]:
				self.accelerate()

			elif key[K_s]:
				self.reverse()

			else:
				self.decelerate()

			if key[K_LCTRL] or key[K_RCTRL]:
				self.shoot()

			if changed:
				self.updateImage()

			self.move()
