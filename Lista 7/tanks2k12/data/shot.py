# -*- encoding: utf8 -*-

import sys
import pygame
from pygame.locals import *
from utils import *

class Shot(AnimatedSprite):
	images = None
	sound = None
	def __init__(self, _pos):
		super(Shot, self).__init__(_pos)
		if not Shot.images:
			Shot.images = loadImages('data/gfx/explosion/', alpha = True)
			for name, image in Shot.images.items():
				Shot.images[name] = pygame.transform.scale(image, (16, 22))

			Shot.sound = loadSound('data/snd/shot.wav')

		self.sound.play()
		self.health = 1
		self.image = self.images['0']
		self.rect = self.image.get_rect()
		self.rect.centerx, self.rect.centery = _pos

	def update(self):
		if not self.health:
			return

		self.nextFrame(self.images)
		if not self.frame:
			self.health = 0
