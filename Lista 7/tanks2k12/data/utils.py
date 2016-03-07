# -*- encoding: utf8 -*-

import os
import math
import time
from collections import defaultdict, deque
from heapq import heappop, heappush
import pygame

FONTS = {}
MAX_MAPSIZE = 64

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

class NoSound:
	def play(self, *args): pass
	def stop(self, *args): pass
	def fadeout(self, *args): pass

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

def loadSound(path):
	if not os.path.exists(path):
		print 'WARNING:', path
		return NoSound()

	return pygame.mixer.Sound(path)

def drawText(surface, text, size, color, (x, y), antialiasing = True):
	if not size in FONTS:
		FONTS[size] = pygame.font.Font(pygame.font.get_default_font(), size)

	render = FONTS[size].render(text, antialiasing, color)
	width, height = render.get_size()
	surface.blit(render, (x - width / 2, y - height / 2))
	return width, height

def loadLevel(path):
	"""Loads level."""

	level = []
	try:
		data = open(path).read().split("\n")
		for line in data:
			if not line:
				continue

			row = []
			for tile in line.split():
				temp = list(map(int, tile.split(';')))
				if len(temp) < 2:
					temp.append(0)

				row.append(tuple(temp))

			level.append(tuple(row))

	except IOError, msg:
		print 'WARNING:', path, msg
		return None

	return tuple(level)

def loadLevels(directory):
	"""Load levels from directory and subdirectories into dict based on path."""

	levels = dictfactory()
	for path, _, files in os.walk(directory):
		if not files:
			continue
	
		act = levels
		for name in path.replace(directory, '').split('/'):
			if name:
				act = act[name]
	
		for filename in files:
			name, ext = os.path.splitext(filename)
			if ext == '.dat':
				act[name] = loadLevel(os.path.join(path, filename))

	return levels

def neighbours(start, passable, maxdist):
	if not passable(start):
		return deque()

	_start = time.time()
	sx, sy = start
	visited = set()
	que = deque()
	res = deque()

	visited.add((0, 0))
	que.append((0, 0))
	res.append(start)
	while que:
		ax, ay = que.popleft()
		for i in (-1, 0, 1):
			if 0 <= sx + ax + i < MAX_MAPSIZE:
				for j in (-1, 0, 1):
					if 0 <= sy + ay + j < MAX_MAPSIZE and abs(ax + i) + abs(ay + j) <= maxdist and not (ax + i, ay + j) in visited and passable((sx + ax + i, sy + ay + j)):
						res.append((sx + ax + i, sy + ay + j))
						que.append((ax + i, ay + j))
						visited.add((ax + i, ay + j))

	return res

def shortPath(start, end, passable):
	_start = time.time()
	processed = set()
	father = [[None for _ in xrange(MAX_MAPSIZE)] for _ in xrange(MAX_MAPSIZE)]
	score = [[2**32 for _ in xrange(MAX_MAPSIZE)] for _ in xrange(MAX_MAPSIZE)]
	que = []
	res = []

	score[start[1]][start[0]] = 0
	que.append((0, start))
	while que:
		_, act = heappop(que)
		if act in processed:
			continue

		if act == end:
			break

		processed.add(act)
		ax, ay = act
		ascore = score[ay][ax]
		for i in (-1, 0, 1):
			if 0 <= ax + i < MAX_MAPSIZE:
				for j in (-1, 0, 1):
					if 0 <= ay + j < MAX_MAPSIZE and passable((ax + i, ay + j)):
						if ascore + distance((0, 0), (i, j)) < score[ay + j][ax + i]:
							father[ax + i][ay + j] = act
							score[ay + j][ax + i] = ascore + distance((0, 0), (i, j))
							heappush(que, (score[ay + j][ax + i] + distance((ax + i, ay + j), end), (ax + i, ay + j)))

	act = end
	while act:
		res.append(act)
		act = father[act[0]][act[1]]
	
	return deque(reversed(res))

#_map = (
#	(0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
#	(0, 1, 1, 1, 1, 1, 1, 1, 1, 0),
#	(0, 1, 1, 1, 1, 1, 1, 1, 1, 0),
#	(0, 1, 1, 1, 1, 1, 1, 1, 1, 0),
#	(0, 1, 1, 1, 1, 1, 1, 1, 1, 0),
#	(0, 1, 1, 1, 1, 1, 1, 1, 1, 0),
#	(0, 1, 1, 1, 1, 1, 1, 1, 1, 0),
#	(0, 1, 1, 1, 1, 1, 1, 0, 1, 0),
#	(0, 1, 1, 1, 1, 1, 1, 1, 1, 0),
#	(0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
#)
#_start, _end = (1, 1), (8, 8)
#_passable = lambda (x, y): 0 <= x < 10 and 0 <= y < 10 and _map[y][x]
#print shortPath(_start, _end, _passable)
#
#def bfsPath(start, end, passable):
#	visited = defaultdict(lambda: False, {})
#	father = {}
#	que = deque()
#	res = []
#	
#	que.append(start)
#	while que:
#		x, y = que.pop(0)
#		for i in (-1, 0, 1):
#			for j in (-1, 0, 1):
#				if not visited[(x + i, y + j)] and passable((x + i, y + j)):
#					que.append((x + i, y + j))
#					visited[(x + i, y + j)] = True
#					father[(x + i, y + j)] = (x, y)
#					if end == (x + i, y + j):
#						break
#
#	if not end in father:
#		return
#
#	act = end
#	while act != start:
#		res.append(act)
#		act = father[act]
#
#	res.append(start)
#	res.reverse()
#	return res
#
#def bfsPaths(end, passable, paths):
#	_size = len(paths[0]), len(paths)
#	visited = [[False for _ in xrange(_size[0])] for _ in xrange(_size[1])]
#	que = deque()
#	que.append(end)
#	visited[end[0]][end[1]] = True
#	if not passable(end):
#		return
#
#	while que:
#		x, y = que.popleft()
#		for i in (-1, 0, 1):
#			if 0 <= x + i < _size[0]:
#				for j in (-1, 0, 1):
#					if 0 <= y + j < _size[1] and not visited[x + i][y + j] and passable((x + i, y + j)):
#						que.append((x + i, y + j))
#						visited[x + i][y + j] = True
#						paths[x + i][y + j][end[0]][end[1]] = (x, y)

