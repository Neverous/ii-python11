# -*- encoding: utf8 -*-

import os
import math
import random
from collections import defaultdict
import pygame

FONTS = {}
class NoMore(Exception): pass

class AnimatedSprite(pygame.sprite.Sprite):
	def __init__(self, (x, y)):
		super(AnimatedSprite, self).__init__()
		self.frame = 0
		self._pos = (x, y)

	def nextFrame(self, frames):
		self.frame += 1
		if self.frame == len(frames):
			self.frame = 0

		self.image = frames[str(self.frame)]
		self.rect = self.image.get_rect()
		self.rect.centerx, self.rect.centery = self._pos

	def getPos(self):
		return self._pos

def dictfactory():
	return defaultdict(dictfactory)

def raise_(exception):
	raise exception

def distance(a, b):
	return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
	
def vectorAngle(v, u):
	angle = (math.atan2(u[1], u[0]) - math.atan2(v[1], v[0])) / math.pi * 180
	if angle < -180: angle += 360
	if angle > 180: angle -= 360

	return angle

def angleVector(angle):
	return -math.sin(angle), math.cos(angle)

def loadImage(path, transparency = None, alpha = False):
	"""Loads image."""
	try:
		image = pygame.image.load(path)
		if alpha:
			image = image.convert_alpha()

		else:
			image = image.convert()

	except pygame.error, msg:
		print 'WARNING:', path, msg
		return None

	if transparency != None:
		if transparency == -1:
			transparency = image.get_at((0, 0))

		image.set_colorkey(transparency, pygame.RLEACCEL)

	return image

def loadImages(directory, transparency = None, alpha = False):
	"""Load images from directory and subdirectories into dict based on path."""

	images = dictfactory()
	for path, _, files in os.walk(directory):
		if not files:
			continue
	
		act = images
		for name in path.replace(directory, '').split('/'):
			if name:
				act = act[name]
	
		for filename in files:
			name = os.path.splitext(filename)[0]
			act[name] = loadImage(os.path.join(path, filename), transparency,
			                      alpha)

	return images

def drawText(surface, text, size, color, (x, y), antialiasing = True):
	if not size in FONTS:
		FONTS[size] = pygame.font.Font(pygame.font.get_default_font(), size)

	render = FONTS[size].render(text, antialiasing, color)
	width, height = render.get_size()
	surface.blit(render, (x - width / 2, y - height / 2))
	return width, height

def randomPlace(reserved, radius, (width, height)):
	free = []
	for x in xrange(radius, width - radius):
		for y in xrange(radius, height - radius):
			add = True
			for obj in reserved:
				if distance(obj.getPos(), (x, y)) < radius + obj.getRadius():
					add = False
					break

			if add:
				free.append((x, y))

	if free:
		return random.choice(free)

	raise NoMore()
