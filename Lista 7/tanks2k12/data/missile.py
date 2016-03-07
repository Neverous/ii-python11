# -*- ecoding: utf8 -*-

import pygame
from utils import *
from explosion import Explosion
import map

EXPLOSION_RANGE = 64
HIT_DAMAGE = 120
SHOOT_RANGE = 300
START_SPEED = 4
MAX_SPEED = 18

class Missile(pygame.sprite.Sprite):
	def __init__(self, _engine, _map, _shooter, _pos, (_vx, _vy), _imaginary = False):
		super(Missile, self).__init__()
		self._engine = _engine
		self._map = _map
		self._shooter = _shooter
		self._pos = list(_pos)
		self._start = _pos
		self._end = (int(self._start[0] + _vx * SHOOT_RANGE), int(self._start[1] + _vy * SHOOT_RANGE))
		self._speed = START_SPEED
		self._vx, self._vy = _vx, _vy
		self._imaginary = _imaginary
		self.health = 1
		self.image = pygame.Surface((3, 3))
		self.rect = self.image.get_rect()
		self.rect.centerx, self.rect.centery = _pos
		self.radius = EXPLOSION_RANGE

	def getPos(self):
		return tuple(self._pos)

	def getEnd(self):
		return self._end

	def update(self):
		self.move()
		if distance(self._start, self._pos) > SHOOT_RANGE:
			self.health = 0

		elif self.health and self._map.getPointField(self._pos)[1] & map.FIELD_BLOCKED:
			self.health = 0

		elif self.health:
			hit = pygame.sprite.spritecollide(self, self._map.tanks, False, pygame.sprite.collide_rect)
			if hit and hit[0] != self._shooter:
				self.health = 0

		if not self.health:
			if not self._imaginary:
				self._map.explosions.add(Explosion(self._pos))

			damaged = pygame.sprite.spritecollide(self, self._map.tanks, False, pygame.sprite.collide_circle)
			for tank in damaged:
				if self._imaginary:
					if tank != self._shooter:
						return tank.getPlayerID() != self._shooter.getPlayerID()

					continue

				tank.hit(max(0, 1.0 * (EXPLOSION_RANGE - distance(tank.getPos(), self._pos)) / EXPLOSION_RANGE * HIT_DAMAGE))

			return True

		if not self._imaginary:
			pygame.draw.circle(self._map.debug, (225, 30, 0), (self.rect.centerx, self.rect.centery), self.radius)
			pygame.draw.line(self._map.debug, (255, 0, 0), self._pos, self._end)

		return None

	def move(self):
		x, y = self._pos
		self._pos = [x + self._speed * self._vx, y + self._speed * self._vy]
		self.rect.centerx, self.rect.centery = self._pos
		self._speed = min(self._speed + 1, MAX_SPEED)
