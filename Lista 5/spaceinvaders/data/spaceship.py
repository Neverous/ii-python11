# -*- encoding: utf8 -*-
import pygame
import random
from pygame.locals import *
from utils import *
from bullet import Bullet
class Spaceship(AnimatedSprite):
	images = None
	def __init__(self, game, x, y, health = 400, cooldown = 0):
		super(Spaceship, self).__init__()
		self.game = game
		self.x = x
		self.y = y
		self.i = 0
		self.health = health
		self.state = 'stop'
		self.cooldown = cooldown
		if not Spaceship.images:
			Spaceship.images = loadImages('data/gfx/ship/', None, True)

		self.image = self.images['stop']
		self.rect = self.image.get_rect()
		self.rect.centerx, self.rect.centery = self.x, self.y

	def move(self, delta = 1):
		self.x += delta
		if self.x < 0: self.x = 0
		elif self.x > 800: self.x = 800

		self.image = self.images[self.state]
		self.rect = self.image.get_rect()
		self.rect.centerx, self.rect.centery = self.x, self.y

	def update(self):
		if self.cooldown:
			self.cooldown -= 1

		pressed = pygame.key.get_pressed()
		if pressed[K_LEFT] and pressed[K_RIGHT]:
			self.state = 'stop'
			delta = 0

		elif pressed[K_LEFT]:
			self.state = 'left'
			delta = -8

		elif pressed[K_RIGHT]:
			self.state = 'right'
			delta = 8

		else:
			self.state = 'stop'
			delta = 0

		self.move(delta)
		if not self.i and pressed[K_LCTRL]:
			self.shoot()

		self.i += 1
		self.i %= 5

	def shoot(self):
		self.game.bullets.add(Bullet(self.game, self.x, self.y, -8, random.randint(50, 75), 0))

	def hit(self, hit, point):
		if self.cooldown:
			return

		self.health -= hit
		if self.health < 0:
			self.health = 0
