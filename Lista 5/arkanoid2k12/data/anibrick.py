# -*- encoding: utf-8 -*-
import pygame

COLORS = (
	(230, 0, 0),
	(0, 230, 0),
	(0, 0, 230),
	(0, 255, 230),
	(230, 230, 0),
)

class AniBrick(pygame.sprite.Sprite):
	def __init__(self, scene, type, pos, size):
		super(AniBrick, self).__init__()
		self.pos = pos
		self.type = type
		self.size = size
		self.image = pygame.Surface(size)
		self.alpha = 30
		self.color = color = list(COLORS[type / 2])
		self.image.fill(color)
		pygame.draw.rect(self.image, [max(0, x - 75) for x in color[:-1]] + [color[-1]] + [self.alpha], (0, 0, size[0], size[1]), 2)
		self.rect = self.image.get_rect()
		self.rect.centerx, self.rect.centery = pos
		self.gone = False
		self.i = self.alpha

	def update(self):
		self.i -= 1
		self.color = [max(0, x * self.i / self.alpha) for x in COLORS[self.type / 2]]
		self.image.fill(self.color)
		pygame.draw.rect(self.image, [max(0, x - 75) for x in self.color], (0, 0, self.size[0], self.size[1]), 2)
		if self.i <= 0:
			self.gone = True

