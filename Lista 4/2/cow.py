# -*- encoding: utf8 -*-
import sys
import math
import random
import pygame
from pygame.locals import *
from utils import *

ALARM_DISTANCE = 100

class Cow(pygame.sprite.Sprite):
	images = None
	def __init__(self, id, game):
		super(Cow, self).__init__()
		if not Cow.images:
			Cow.images = loadImages('data/cow/', -1)

		self.id = id
		self.game = game
		self.x, self.y = random.randint(1, 640), random.randint(1, 480)
		self.h, self.v = '', 's'
		self.action = 'eat'
		self.frame = 0
		self.image = self.images[self.getAction()][self.getDirection() + str(self.frame)]
		self.rect = self.image.get_rect()
		self.rect.centerx, self.rect.centery = self.x, self.y
		self.i = 0
		self.patiency = random.randint(200, 500) 
		self.inside = False
		self.borders = (0, 0), (640, 480)
		self.randomSpeed()

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
		if self.inside:
			x /= 1.5
			y /= 1.5

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
		if self.x < self.borders[0][0]: self.x = self.borders[0][0]
		elif self.x > self.borders[1][0]: self.x = self.borders[1][0]

		if self.y < self.borders[0][1]: self.y = self.borders[0][1]
		elif self.y > self.borders[1][1]: self.y = self.borders[1][1]

		self.rect.centerx, self.rect.centery = self.getPosition()
		if not self.inside and 0 < self.x - self.game.farm[0][0] < self.game.farm[1][0] and\
			0 < self.y - self.game.farm[0][1] < self.game.farm[1][1]:
			self.inside = True
			self.borders = self.game.farm[0], (self.game.farm[1][0] + self.game.farm[0][0], self.game.farm[1][1] + self.game.farm[0][1])
			self.game.result = (self.game.result[0] + 1, self.game.result[1])

	def randomSpeed(self):
		self.vx = random.randint(-2000, 2000) / 1000.0
		self.vy = random.randint(-2000, 2000) / 1000.0

	def update(self):
		if not self.inside:
			dist = distance(self.game.shepherds[0].getPosition(), self.getPosition())
			nearest = self.game.shepherds[0]
			for n, shepherd in enumerate(self.game.shepherds):
				act = distance(shepherd.getPosition(), self.getPosition())
				if act < dist:
					dist = act
					nearest = shepherd

			if dist < ALARM_DISTANCE:
				self.patiency = random.randint(200, 500)
				sx, sy = nearest.getPosition()
				x, y = self.getPosition()
				vx, vy = x - sx, y - sy
				angle = random.randint(-45, 45) * math.pi / 180
				vx, vy = vx * math.cos(angle) - vy * math.sin(angle), vx * math.sin(angle) + vy * math.cos(angle)
				length = math.sqrt(vx ** 2 + vy ** 2) / random.randint(1, 2000) * 1000.0
				vy /= length
				vx /= length
				self.vy = vy
				self.vx = vx

		if self.patiency > 0:
			self.patiency -= 1

		else:
			if random.randint(1, 20) == 20:
				self.patiency = random.randint(150, 300)
				self.vx, self.vy = 0, 0
			
			else:
				self.patiency = random.randint(200, 500)
				self.randomSpeed()
			
		if abs(self.vx) > 0.01 or abs(self.vy) > 0.01:
			self.action = 'walk'

		else:
			self.action = 'eat'

		self.move(self.vx, self.vy)
		x, y = self.getPosition()
		if self.vx < 0 and self.x - self.borders[0][0] < 0.5:
			self.vx = -self.vx

		if self.vx > 0 and self.borders[1][0] - self.x < 0.5:
			self.vx = -self.vx

		if self.vy < 0 and self.y - self.borders[0][1] < 0.5:
			self.vy = -self.vy

		if self.vy > 0 and self.borders[1][1] - self.y < 0.5:
			self.vy = -self.vy

		self.i += 1
		if self.i > 5: # 1/5 FPS
			self.nextFrame()
			self.i = 0
