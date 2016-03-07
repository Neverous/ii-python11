# -*- encoding: utf-8 -*-
import pygame

class Paddle(pygame.sprite.Sprite):
	def __init__(self, scene, pos):
		super(Paddle, self).__init__()
		self.image = pygame.Surface((100, 16))
		self.scene = scene
		self.image.fill((255, 255, 255))
		self.rect = self.image.get_rect()
		self.rect.centerx, self.rect.centery = pos
		self.gone = False

	def move(self, pos):
		resx, _ = self.scene.engine.getResolution()
		width, _ = self.image.get_size()
		if pos < width / 2:
			pos = width / 2

		if pos > resx - width / 2:
			pos = resx - width / 2

		self.rect.centerx = pos

	def update(self):
		pass

	def hit(self, points):
		pass
