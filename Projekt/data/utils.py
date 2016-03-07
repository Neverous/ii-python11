# -*- encoding: utf8 -*-
# Maciej Szeptuch

import os
import math
import time
import cPickle as pickle
from collections import defaultdict, deque
from heapq import heappop, heappush
import pygame
import field

## BUFOR CZCIONEK
FONTS = {}

## BUFOR OBRAZKÓW
IMAGES = {}

## BUFOR DŹWIĘKÓW
SOUNDS = {}

class NoSound:
	"""Obiekt reprezentujący brak dźwięku."""

	def play(self, *args): pass
	def stop(self, *args): pass
	def fadeout(self, *args): pass

def dictfactory():
	"""Nieskończony słownik."""

	return defaultdict(dictfactory)

def raise_(exception):
	"""Rzucanie wyjątku w formie funkcji. Przydatne do lambd."""

	raise exception

def loadImage(path, transparency = None, alpha = False):
	"""Wczytywanie obrazka dla pygame."""

	_id = path + ':' + str(transparency) + ':' + str(alpha)
	if IMAGES.has_key(_id):
		return IMAGES[_id]

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

	IMAGES[_id] = image
	return image

def loadImages(directory, transparency = None, alpha = False):
	"""Wczytywanie obrazków z folderu do słownika."""

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
	"""Wczytuje dźwięk dla pygame."""

	if SOUNDS.has_key(path):
		return SOUNDS[path]

	if not os.path.exists(path):
		print 'WARNING:', path
		return NoSound()

	SOUNDS[path] = pygame.mixer.Sound(path)
	return SOUNDS[path]

def drawText(surface, text, size, color, (x, y), antialiasing = True):
	"""Wypisuje tekst na ekranie, wyśrodkowany w pkt. (x, y)."""
	if not size in FONTS:
		FONTS[size] = pygame.font.Font(pygame.font.get_default_font(), size)

	renders = []
	width = 0
	height = 0
	for line in text.split("\n"):
		render = FONTS[size].render(line, antialiasing, color)
		renders.append(render)
		w, h = render.get_size()
		width = max(width, w)
		height += h

	act = 0
	for render in renders:
		w, h = render.get_size()
		surface.blit(render, (x - w / 2, y - height / 2 + act))
		act += h

	return x - width / 2, y - height / 2, width, height

def distance(a, b):
	"""Odległość między dowma punktami w 2d."""

	return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def vectorAngle(v, u):
	angle = (math.atan2(u[1], u[0]) - math.atan2(v[1], v[0])) / math.pi * 180
	if angle < -180: angle += 360
	if angle > 180: angle -= 360

	return angle

def neighbours(start, passable, maxdist, MAX_MAPSIZE = 32):
	"""DFS - zwraca najbliższych sąsiadów."""

	if not passable(start):
		return deque()

	sx, sy = start
	visited = set()
	que = deque()
	res = deque()

	visited.add((0, 0))
	que.append((0, 0))
	res.append(start)
	while que:
		ax, ay = que.popleft()
		for (i, j) in ((-1, 0), (1, 0), (0, 1), (0, -1)):
			if 0 <= sx + ax + i < MAX_MAPSIZE and 0 <= sy + ay + j < MAX_MAPSIZE and abs(ax + i) + abs(ay + j) <= maxdist and not (ax + i, ay + j) in visited and passable((sx + ax + i, sy + ay + j)):
				res.append((sx + ax + i, sy + ay + j))
				que.append((ax + i, ay + j))
				visited.add((ax + i, ay + j))

	return res

def shortPath(start, end, passable, MAX_MAPSIZE = 32):
	"""A* zwraca najkrótszą ścieżkę między punktami."""

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
		for (i, j) in ((-1, 0), (1, 0), (0, 1), (0, -1)):
			if 0 <= ax + i < MAX_MAPSIZE and 0 <= ay + j < MAX_MAPSIZE and passable((ax + i, ay + j)) and ascore + distance((0, 0), (i, j)) < score[ay + j][ax + i]:
				father[ax + i][ay + j] = act
				score[ay + j][ax + i] = ascore + distance((0, 0), (i, j))
				heappush(que, (score[ay + j][ax + i] + distance((ax + i, ay + j), end), (ax + i, ay + j)))

	act = end
	while act:
		res.append(act)
		act = father[act[0]][act[1]]
	
	return deque(reversed(res))

def loadLevel(path):
	"""Wczytuje poziom."""

	try:
		return pickle.load(open(path, 'rb'))

	except (IOError, EOFError):
		return None

def saveLevel(path, level):
	"""Zapisuje poziom."""

	while len(level) > 1 and emptyStorey(level[0]):
		del level[0]

	while len(level) > 1 and emptyStorey(level[-1]):
		del level[-1]

	return pickle.dump(level, open(path, 'wb'), -1)

def emptyStorey(storey):
	"""Czy poziom jest pusty?"""

	for row in storey:
		for cell in row:
			if type(cell) != field.Field:
				return False

			if cell.getModifier():
				return False

	return True
