# -*- encoding: utf8 -*-
import random
import pygame
from pygame.locals import *
from utils import *
import gamestate
from bullet import Bullet
HEALTH = (0, 50, 100, 150, 200, 225, 300)
class Invader(AnimatedSprite):
	images = None
	def __init__(self, game, x, y, type = '1'):
		super(Invader, self).__init__()
		self.i = 0
		self.mod = random.randint(2, 4)
		self.game = game
		self.abs = 0
		self.delta = 3
		self.x = x
		self.y = y
		self.type = type
		self.health = HEALTH[int(type)]
		if not Invader.images:
			Invader.images = loadImages('data/gfx/invader/', None, True)

		self.image = self.images[type]['0']
		self.rect = self.image.get_rect()
		self.rect.centerx, self.rect.centery = self.x, self.y

	def update(self):
		if random.randint(1, 700 / int(self.type)) == 5:
			self.shoot()

		self.move()
		if not self.i:
			self.nextFrame(self.images[self.type])

		if self.y > 520:
			raise gamestate.GameOver()

		self.i += 1
		self.i %= self.mod

	def move(self):
		self.abs += self.delta
		self.x += self.delta
		self.y += 1.0 * abs(self.delta) / 10
		if abs(self.abs) >= 96:
			self.delta *= -1

	def shoot(self):
		self.game.bullets.add(Bullet(self.game, self.x, self.y, random.randint(1, 3) + int(self.type), random.randint(5, 25) * int(self.type)))

	def hit(self, hit, point):
		self.health -= hit
		self.game.score += hit / 10
		if self.health < 0:
			self.health = 0
