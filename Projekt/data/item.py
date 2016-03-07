# -*- encoding: utf8 -*-
# Maciej Szeptuch 2012

from collections import defaultdict
import pygame
from pygame.locals import *
import utils

class Item(pygame.sprite.Sprite):
	"""Przedmiot."""

	@classmethod
	def randomize(cls):
		"""Losuje przedmiot."""

		return Item()

	def __init__(self, _image = 'unknown'):
		super(Item, self).__init__()
		self.image = utils.loadImage(_image, alpha = True)
		self.rect = self.image.get_rect()
		self._detached = False
		self._attached = None # obiekt do którego przypięty jest przedmiot(skrzynia, pole, komórka w ekwipunku)
		self.stats = defaultdict(lambda: 0)

	def getAttached(self):
		"""Zwraca nadrzędny obiekt."""

		return self._attached
	
	def detach(self):
		"""Odpina przedmiot."""

		self._detached = True
		self._attached.gotItem()

	def attach(self, _place):
		"""Przypina przedmiot do _place."""

		self.kill()
		if not _place or not _place.putItem(self):
			return False

		self.rect.center = (-1000, -1000) # trzeba go wyrzucić poza obszar rysowania(żeby nie wisiał w dziwnym miejscu póki się ekran nie odświeży)
		self._attached = _place
		self._detached = False
		return True

	def getDescription(self):
		return "Unknown"

	def update(self):
		if not self._detached:
			return []

		return [tuple(self.rect)]

	def mouseEvent(self, event):
		if event.type == MOUSEMOTION:
			self.rect.center = event.pos

	def draw(self, surface):
		surface.blit(self.image, self.rect.topleft)
