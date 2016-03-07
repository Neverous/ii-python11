# -*- encoding: utf8 -*-

import sys
import pygame
from pygame.locals import *
from utils import *

class Explosion(AnimatedSprite):
	images = None
	sound = None
	def __init__(self, _pos):
		super(Explosion, self).__init__(_pos)
		if not Explosion.images:
			Explosion.images = loadImages('data/gfx/explosion/', alpha = True)
			Explosion.sound = loadSound('data/snd/explosion.wav')

		self.health = 1
		self.image = self.images['0']
		self.rect = self.image.get_rect()
		self.rect.centerx, self.rect.centery = self._pos
		self.sound.play()

	def update(self):
		if not self.health:
			return

		self.nextFrame(self.images)
		if not self.frame:
			self.health = 0
