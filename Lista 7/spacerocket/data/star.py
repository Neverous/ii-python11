# -*- encoding: utf8 -*-

import pygame
from utils import *

class Star(AnimatedSprite):
	images = None
	def __init__(self, pos):
		super(Star, self).__init__(pos)

		if not Star.images:
			Star.images = loadImages('data/gfx/star/', alpha = True)
		
		self.image = Star.images['0']
		self.rect = self.image.get_rect()
		self.rect.centerx, self.rect.centery = pos
		self.radius = 16
		self.mass = 30

	def getPos(self):
		return self.rect.centerx, self.rect.centery

	def getRadius(self):
		return self.radius

	def update(self):
		self.nextFrame(Star.images)
