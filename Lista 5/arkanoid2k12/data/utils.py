# -*- encoding: utf8 -*-
import os
import math
from collections import defaultdict
import pygame

def loadImage(path, transparency = None, alpha = False):
	"""Loads image."""
	try:
		image = pygame.image.load(path)
		if alpha:
			image = image.convert_alpha()

		else:
			image = image.convert()

	except pygame.error, msg:
		print 'WARNING: ', msg
		return None

	if transparency != None:
		if transparency == -1:
			transparency = image.get_at((0, 0))

		image.set_colorkey(transparency, pygame.RLEACCEL)

	return image

def loadImages(directory, transparency = None, alpha = False):
	"""Load images from directory and subdirectories into dict based on path."""

	def factory():
		return defaultdict(factory)

	images = factory()
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

def distance(A, B):
	return math.sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2)

class AnimatedSprite(pygame.sprite.Sprite):
	images = None
	def __init__(self):
		super(AnimatedSprite, self).__init__()
		self.frame = 0

	def nextFrame(self, frames):
		self.frame += 1
		if self.frame == len(frames):
			self.frame = 0

		self.image = frames[str(self.frame)]
		self.rect = self.image.get_rect()
		self.rect.centerx, self.rect.centery = self.x, self.y

def loadLevel(path):
	"""Load level from file."""

	return tuple(map(lambda line: tuple([int(num) for num in line]), open(path).read().split("\n")[:-1]))

def loadLevels(directory):
	"""Load levels from directory"""

	levels = {}
	for path, _, files in os.walk(directory):
		if not files:
			continue
	
		for filename in files:
			name = int(os.path.splitext(filename)[0])
			levels[name] = loadLevel(os.path.join(path, filename))

	return levels

class NoSound:
	def play(self, *args):
		pass

	def stop(self, *args):
		pass

	def fadeout(self, *args):
		pass

def loadSound(dir):
	if not os.path.exists(dir):
		return NoSound()

	return pygame.mixer.Sound(dir)
