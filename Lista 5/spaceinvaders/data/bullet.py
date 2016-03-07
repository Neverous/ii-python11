# -*- encoding: utf8 -*-
import sys
import pygame
from pygame.locals import *
from utils import *
from explosion import Explosion
class Bullet(pygame.sprite.Sprite):
	sound = None
	def __init__(self, game, x, y, delta, hit, type = 1):
		super(Bullet, self).__init__()
		self.game = game
		self.x = x
		self.y = y
		self.type = type
		self.delta = delta
		self.health = hit
		if not Bullet.sound:
			Bullet.sound = pygame.mixer.Sound('data/snd/bullet.wav')

		self.image = loadImage('data/gfx/bullet.png', None, True)
		self.rect = self.image.get_rect()
		self.rect.centerx, self.rect.centery = self.x, self.y
		self.sound.play()

	def update(self):
		# ASTEROIDS
		hit = []
		hit.extend(pygame.sprite.spritecollide(self, self.game.asteroids, False, pygame.sprite.collide_mask))
		if self.type:
			hit.extend(pygame.sprite.spritecollide(self, self.game.player, False, pygame.sprite.collide_mask))

		else:
			hit.extend(pygame.sprite.spritecollide(self, self.game.invaders, False, pygame.sprite.collide_mask))

		if hit:
			for sprite in hit:
				sprite.hit(self.health, (self.x, self.y))
				self.game.explosions.add(Explosion(self.game, self.x, self.y))

			self.health = 0

		else:
			self.move()

	def move(self):
		self.y += self.delta
		self.rect.centerx, self.rect.centery = self.x, self.y
		if not 0 <= self.y <= self.game.y or not 0 <= self.x <= self.game.x:
			self.health = 0
