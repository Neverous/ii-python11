# -*- encoding: utf-8 -*-
import random
import pygame
from anibrick import AniBrick
from bonus import Bonus

COLORS = (
	(255, 0, 0),
	(0, 255, 0),
	(0, 0, 255),
	(0, 255, 255),
	(255, 255, 0),
)

class Brick(pygame.sprite.Sprite):
	def __init__(self, scene, type, pos, size):
		super(Brick, self).__init__()
		self.pos = pos
		self.type = type
		self.size = size
		self.scene = scene
		self.life = (type + 1) * 10
		self.image = pygame.Surface(size)
		color = COLORS[type / 2]
		self.image.fill(color)
		pygame.draw.rect(self.image, [max(0, x - 75) for x in color], (0, 0, size[0], size[1]), 2)
		self.rect = self.image.get_rect()
		self.rect.centerx, self.rect.centery = pos
		self.gone = False

	def update(self):
		pass

	def hit(self, points):
		self.life -= points
		if self.life <= 0:
			self.gone = True
			self.scene.engine.player['score'] += (self.type + 1) * 10
			self.scene.anibricks.add(AniBrick(self.scene, self.type, self.pos, self.size))
			if self.type % 2 == 0 and random.randint(0, 1):
				self.scene.bonus.add(Bonus(self.scene, self.pos))

