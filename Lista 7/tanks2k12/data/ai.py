# -*- encoding: utf8 -*-

import math
import time
import random
import cPickle as pickle
from collections import defaultdict, deque
import pygame
from utils import *
import tank
import map
import missile
from missile import Missile

class Area(pygame.sprite.Sprite):
	def __init__(self, pos, radius):
		super(Area, self).__init__()
		self.rect = pygame.Rect(0, 0, 32, 32)
		self.rect.centerx, self.rect.centery = pos
		self.radius = radius

class AI(object):
	_shortestpath = None
	def __init__(self, _engine, _map, _player, _id):
		super(AI, self).__init__()
		self._engine = _engine
		self._map = _map
		self._gridmask = self._map.getGridMasks()
		self._id = _id
		self._player = _player
		self._opponent = self._engine.players[_id ^ 1]
		self._mapsize = self._map.getSize()
		_size = (self._mapsize[0] / 32, self._mapsize[1] / 32)
		temp = self._player['flag'].getPos()
		self._defense = neighbours((temp[0] / 32, temp[1] / 32), lambda (x, y): not self._gridmask[y][x] & map.FIELD_BLOCKED, 8)
		temp = self._opponent['flag'].getPos()
		self._offense = neighbours((temp[0] / 32, temp[1] / 32), lambda (x, y): not self._gridmask[y][x] & map.FIELD_BLOCKED, 4)
		self._midlane = tuple(filter(lambda (x, y): not self._gridmask[y][x] & map.FIELD_BLOCKED, [(x, y) for x in xrange(self._mapsize[0] / 64 - 16, self._mapsize[0] / 64 + 16) for y in xrange(self._mapsize[1] / 64 - 16, self._mapsize[1] / 64 + 16)]))
		self._pgx, self._pgy = 0, 0
		self._data = dictfactory()

	def update(self):
		for tnk in self._player['tanks']:
			if tnk.focus:
				continue

			if not self._engine.timeLeft()[0] < 3 and random.randint(1, 3) == 2:
				self._data[tnk]['role'] = random.randint(1, 5)

			if not self._data[tnk]['role']:
				self._data[tnk]['role'] = random.randint(1, 5)

			self.shootArea(tnk)
			if tnk.repair and (tnk.health < tank.MAX_HEALTH * 0.75 or tnk.missiles < 15):
				continue

			if not tnk.repair and (tnk.health < tank.MAX_HEALTH * 0.25 or tnk.missiles < 5):
				self.workshopTarget(tnk)

			else:
				if tnk.flagged:
					self.escapeTarget(tnk)

				elif self._data[tnk]['role'] == 1:
					self.defenseTarget(tnk)

				elif self._data[tnk]['role'] in (2, 3):
					self.middleTarget(tnk)

				elif self._data[tnk]['role'] == 4:
					self.offenseTarget(tnk)

				elif self._data[tnk]['role'] == 5:
					self.flagSecureTarget(tnk)

			self.calculatePath(tnk)
			self.collisionPrevention(tnk)
			self.tryMove(tnk)

	def collisionPrevention(self, tnk):
		if random.randint(1, 4) != 2:
			return

		tankData = self._data[tnk]
		pygame.draw.circle(self._map.debug, (0, 200, 255), (int(tnk.getPos()[0]), int(tnk.getPos()[1])), 128)
		radar = set([(int(t.getPos()[0] / 32), int(t.getPos()[1] / 32)) for t in pygame.sprite.spritecollide(Area(tnk.getPos(), 128), self._map.tanks, False, pygame.sprite.collide_circle) if t != tnk])
		for point in tankData['path']:
			if point in radar:
				break

		else:
			return

		self.calculatePath(tnk, radar)
		if tankData['path']:
			tankData['path'].popleft()

	def shootArea(self, tnk):
		opponents = [t.getPos() for t in pygame.sprite.spritecollide(Area(tnk.getPos(), missile.SHOOT_RANGE), self._opponent['tanks'], False, pygame.sprite.collide_circle)]
		if not opponents:
			return

		x, y = tnk.getPos()
		bx, by = angleVector(2.0 * math.pi * tnk.barrel / 32)
		opponents.sort(key = lambda (ox, oy): abs(vectorAngle((bx, by), (ox - x, oy - y))))
		for dx, dy in opponents:
			mis = Missile(self._engine, self._map, tnk, (x + 20 * bx, y + 20 * by), (bx, by), True)
			canshoot = False
			while True:
				temp = mis.update()
				if temp == None:
					continue

				if temp == False:
					break

				if temp == True:
					canshoot = True
					break

			if canshoot:
				break

		angle = vectorAngle((bx, by), (dx - x, dy - y))
		if abs(angle) < 12 and random.randint(1, 5) == 3:
			tnk.shoot()

		if angle > 11:
			tnk.barrelRight()

		elif angle < -11:
			tnk.barrelLeft()

		if abs(angle) < 12 and random.randint(1, 5) == 3:
			tnk.shoot()

		tnk.updateImage()

	def workshopTarget(self, tnk):
		tankData = self._data[tnk]
		wx, wy = self._player['workshop'].getPos()
		wx = int(wx / 32)
		wy = int(wy / 32)
		if self._player['workshop'].occupied:
			if tankData['target'] and distance(tankData['target'], (wx, wy)) > 20:
				tankData['target'] = random.choice(neighbours((wx, wy), lambda (x, y): not self._gridmask[y][x] & map.FIELD_BLOCKED, 16))
				tankData['path'] = deque()

		elif not tankData['target'] or distance(tankData['target'], (wx, wy)) > 5:
			tankData['target'] = (wx, wy)
			tankData['path'] = deque()

	def escapeTarget(self, tnk):
		if not self._data[tnk]['target']:
			fx, fy = self._player['flag'].getPos()
			self._data[tnk]['target'] = (int(fx / 32), int(fy / 32))

	def defenseTarget(self, tnk):
		if not self._data[tnk]['target']:
			self._data[tnk]['target'] = random.choice(self._defense)

	def middleTarget(self, tnk):
		if not self._data[tnk]['target']:
			rand = random.randint(1, 5)
			if rand == 3:
				return self.offenseTarget(tnk)

			elif rand == 5:
				return self.defenseTarget(tnk)

			self._data[tnk]['target'] = random.choice(self._midlane)

	def offenseTarget(self, tnk):
		if not self._data[tnk]['target']:
			self._data[tnk]['target'] = random.choice(self._offense)

	def flagSecureTarget(self, tnk):
		if not self._data[tnk]['target']:
			try:
				fx, fy = filter(lambda t: t.flagged, self._player['tanks'])[0].getPos()
				self._data[tnk]['target'] = (int(fx / 32), int(fy / 32))

			except:
				if random.randint(1, 3) == 2:
					self.offenseTarget(tnk)

				else:
					self.middleTarget(tnk)

	def calculatePath(self, tnk, radar = set()):
		tankData = self._data[tnk]
		if not tankData['target'] or (not radar and tankData['path']):
			return

		px, py = tnk.getPos()
		px = int(px / 32)
		py = int(py / 32)
		tankData['path'] = shortPath((px, py), tankData['target'], lambda (x, y): not self._gridmask[y][x] & map.FIELD_BLOCKED and not (x, y) in radar)

	def tryMove(self, tnk):
		tankData = self._data[tnk]
		if tankData['sleep']:
			tankData['sleep'] -= 1
			return

		if not tankData['target'] or not tankData['path'] or tankData['sleep']:
			return

		ax, ay = tnk.getPos() # actual point
		pts = [(ax, ay)] + [(x * 32 + 16, y * 32 + 16) for x, y in tankData['path']]
		agx, agy = int(ax / 32), int(ay / 32) # actual grid
		tgx, tgy = tankData['target'] # target grid
		tx = tgx * 32 + 16; ty = tgy * 32 + 16 # target point
		pgx, pgy = tankData['path'][0]
		px, py = pgx * 32 + 16, pgy * 32 + 16 # temporary target point

		bx, by = angleVector(2.0 * math.pi * tnk.tracks / 32) # tracks direction vector
		angle = vectorAngle((bx, by), (px - ax, py - ay)) # angle to temporary point

		if angle > 11:
			tnk.turnRight()
			tnk.decelerate()

		elif angle < -11:
			tnk.turnLeft()
			tnk.decelerate()

		if abs(angle) < 46 or abs(angle) > 100:
			if abs(angle) > 100:
				tnk.reverse()

			else:
				tnk.accelerate()

			if not tnk.move():
				if abs(angle) < 46:
					tnk.fullreverse()

				else:
					tnk.fullaccelerate()

				_start = time.time()
				tx, ty = tnk.getPos()
				tgx, tgy = int(tx / 32), int(ty / 32)
				radar = set([(int(t.getPos()[0] / 32), int(t.getPos()[1] / 32)) for t in pygame.sprite.spritecollide(Area(tnk.getPos(), 128), self._map.tanks, False, pygame.sprite.collide_circle) if t != tnk])

				pygame.draw.circle(self._map.debug, (0, 225, 30), (int(tnk.getPos()[0]), int(tnk.getPos()[1])), 128)
				if not tankData['original']:
					tankData['original'] = tankData['target']

				tankData['target'] = random.choice(tuple(filter(lambda (x, y): not self._gridmask[y][x] & map.FIELD_BLOCKED and not (x, y) in radar, neighbours((tgx, tgy), lambda _: True, 6))))
				tankData['path'] = deque()
				self.calculatePath(tnk, radar)
				if tankData['path'] and tankData['path'][0] == (tgx, tgy):
					tankData['path'].popleft()

				tankData['target'] = tankData['original']
				tankData['sleep'] = random.randint(1, 10)

			elif distance(tnk.getPos(), (tx, ty)) < 2:
				tankData['target'] = None
				tankData['original'] = None
				tankData['path'] = deque()

			elif distance(tnk.getPos(), (px, py)) < 8:
				tankData['path'].popleft()

		tnk.updateImage()
		pygame.draw.lines(self._map.debug, (0, 255, 0), False, pts)
