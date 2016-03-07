# -*- encoding: utf8 -*-
import sys
import pygame
from pygame.locals import *
from utils import *
class Explosion(AnimatedSprite):
	images = None
	sound = None
	def __init__(self, game, x, y):
		super(Explosion, self).__init__()
		self.game = game
		self.x = x
		self.y = y
		self.health = 1
		if not Explosion.images:
			Explosion.images = loadImages('data/gfx/explosion/', None, True)
			Explosion.sound = pygame.mixer.Sound('data/snd/explosion.wav')

		self.image = self.images['0']
		self.rect = self.image.get_rect()
		self.rect.centerx, self.rect.centery = self.x, self.y
		self.sound.play()

	def update(self):
		self.nextFrame(self.images)
		if not self.frame:
			self.health = 0
