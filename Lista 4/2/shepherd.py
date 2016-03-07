# -*- encoding: utf8 -*-
import sys
import math
import random
import pygame
from pygame.locals import *
from utils import *
class Shepherd(pygame.sprite.Sprite):
	images = None
	def __init__(self, id, game):
		super(Shepherd, self).__init__()
		if not Shepherd.images:
			Shepherd.images = loadImages('data/shepherd/', -1)

		self.id = id
		self.game = game
		self.x, self.y = random.randint(1, 640), random.randint(1, 480)
		self.h, self.v = '', 's'
		self.action = 'stop'
		self.frame = 0
		self.image = self.images[self.getAction()][self.getDirection() + str(self.frame)]
		self.rect = self.image.get_rect()
		self.rect.centerx, self.rect.centery = self.x, self.y
		self.i = 0

	def getDirection(self):
		return (self.v + self.h) or 's'

	def getPosition(self):
		return (self.x, self.y)

	def getAction(self):
		return self.action

	def nextFrame(self):
		self.frame += 1
		self.image = self.images[self.getAction()][self.getDirection() + str(self.frame)]
		if not isinstance(self.image, pygame.Surface):
			self.frame = 0
			self.image = self.images[self.getAction()][self.getDirection() + str(self.frame)]

		self.rect = self.image.get_rect()
		self.rect.centerx, self.rect.centery = self.getPosition()

	def move(self, x, y):
		if x > 0: self.h = 'e'
		elif x < 0: self.h = 'w'
		else: self.h = ''

		if y > 0: self.v = 's'
		elif y < 0: self.v = 'n'
		else: self.v = ''

		if x and y:
			x /= math.sqrt(2)
			y /= math.sqrt(2)

		self.x += x
		self.y += y
		if self.x < 0: self.x = 0
		elif self.x > 640: self.x = 640

		if self.y < 0: self.y = 0
		elif self.y > 480: self.y = 480

		self.rect.centerx, self.rect.centery = self.getPosition()

	def update(self):
		if self.id == self.game.shepherd:
			pressed = pygame.key.get_pressed()
			if True in (pressed[K_UP], pressed[K_LEFT], pressed[K_DOWN], pressed[K_RIGHT]):
				self.action = 'walk'
				delta = 2
				x, y = 0, 0
				if pressed[K_UP]: y = -delta
				elif pressed[K_DOWN]: y = delta

				if pressed[K_LEFT]: x = -delta
				elif pressed[K_RIGHT]: x = delta

				self.move(x, y)

			else:
				self.action = 'stop'

		self.i += 1
		if self.i > 3: # 1/3 FPS
			self.nextFrame()
			self.i = 0
