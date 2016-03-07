# -*- encoding: utf8 -*-

import pygame
from pygame.locals import *
from utils import *
import planet

MAX_FUEL = 500

class Rocket(pygame.sprite.Sprite):
	images = None
	def __init__(self, _engine, _scene, pos):
		super(Rocket, self).__init__()
		self._engine = _engine
		self._scene = _scene

		if not Rocket.images:
			Rocket.images = loadImages('data/gfx/rocket/', alpha = True)

		self._state = 'off'
		self.image = Rocket.images['off']
		self.rect = self.image.get_rect()
		self._pos = list(pos)
		self._vx, self._vy = 0, 0
		self._resx, self._resy = self._engine.getResolution()
		self.rect.centerx, self.rect.centery = pos
		self._angle = 0
		self.radius = 48
		self._before = (0, 0)

	def getPos(self):
		return tuple(self._pos)

	def update(self):
		self.gravity()
		for star in pygame.sprite.spritecollide(self, self._scene.stars, True, pygame.sprite.collide_mask):
			self._engine.game['score'] += self._engine.game['fuel']

		for canister in pygame.sprite.spritecollide(self, self._scene.canisters, True, pygame.sprite.collide_mask):
			self._engine.game['fuel'] = min(self._engine.game['fuel'] + 135, MAX_FUEL)

		pressed = pygame.key.get_pressed()
		if pressed[K_LEFT] or pressed[K_a]:
			self.turnLeft()

		elif pressed[K_RIGHT] or pressed[K_d]:
			self.turnRight()

		if pressed[K_UP] or pressed[K_w]:
			if self.accelerate():
				self._state = 'on'

			else:
				self._state = 'off'

		else:
			self._state = 'off'

		self.updateImage()
		self.move()

	def gravity(self):
		for p in self._scene.planets:
			x, y = p.getPos()
			d = distance(p.getPos(), self._pos)
			if d < p.getRadius():
				continue

			a = p.mass / (d ** 2) * planet.GRAVITY
			vx, vy = x - self._pos[0], y - self._pos[1]
			d = distance((vx, vy), (0, 0))
			vx /= d; vx *= a
			vy /= d; vy *= a
			self._vx += vx
			self._vy += vy

	def turnLeft(self):
		self._angle += 5
		if self._angle >= 360:
			self._angle -= 360

	def turnRight(self):
		self._angle -= 5
		if self._angle <= 0:
			self._angle += 360

	def updateImage(self):
		if self._before == (self._state, self._angle):
			return

		self._before = (self._state, self._angle)
		self.image = pygame.transform.rotate(self.images[self._state], (self._angle + 270) % 360)
		self.rect = self.image.get_rect()
		self.rect.centerx, self.rect.centery = self._pos

	def accelerate(self):
		if not self._engine.game['fuel']:
			return False

		if self._engine.game['godlevel'] != self._engine.game['level']:
			self._engine.game['fuel'] = max(self._engine.game['fuel'] - random.randint(1, 5), 0)

		vx, vy = angleVector(self._angle * math.pi / 180)
		self._vx -= vx * 0.5
		self._vy += vy * 0.5
		return True

	def move(self):
		self._pos = [self._pos[0] + self._vx, self._pos[1] + self._vy]
		self.rect.centerx, self.rect.centery = self._pos

		hit = pygame.sprite.spritecollide(self, self._scene.planets, False, pygame.sprite.collide_circle)
		if hit:
			if self._engine.game['godlevel'] != self._engine.game['level']:
				dmg = 0
				for p in hit:
					dmg += math.sqrt(self._vx ** 2 + self._vy ** 2 - 2 * self._vx * self._vy * math.cos(self._angle * math.pi / 180))
				
				self._engine.game['life'] -= int(dmg / 10)

			self._vx *= -1
			self._vy *= -1
			self._pos = [self._pos[0] + self._vx, self._pos[1] + self._vy]
			self._vx *= 0.75
			self._vy *= 0.75

		if self._pos[0] < -48:
			self._pos[0] = self._resx + 48

		if self._pos[0] > self._resx + 48:
			self._pos[0] = -48

		if self._pos[1] < -48:
			self._pos[1] = self._resy + 48

		if self._pos[1] > self._resy + 48:
			self._pos[1] = -48
