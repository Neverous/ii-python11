# -*- encoding: utf8 -*-
import sys
import pygame
from pygame.locals import *
import cPickle as pickle

colors = (
	(0, 0, 0),
	(255, 0, 0),
	(0, 255, 0),
	(0, 0, 255),
	(255, 255, 0),
	(255, 0, 255),
	(0, 255, 255),
	(255, 255, 255),
)

try:
	data = pickle.load(open('image.dat', 'r'))

except:
	data = [[(255, 255, 255)] * 64 for r in range(48)]

hi = 0
history = [] # changes (x, y, colorBefore, colorAfter)
def updateImage(pos, size, color):
	c = pos[0] / 10
	r = pos[1] / 10
	hist = []
	for i in range(max(0, r - size / 2), min(48, r + size / 2 + 1)):
		for j in range(max(0, c - size / 2), min(64, c + size / 2 + 1)):
			if data[i][j] != color:
				hist.append((i, j, data[i][j], color))
				data[i][j] = color

	if hist:
		global history, hi
		if len(history) > hi:
			history = history[:hi]

		hi += 1
		history.append(hist)

def fillImage(pos, color):
	c = pos[0] / 10
	r = pos[1] / 10
	base = data[r][c]
	hist = []
	que = [(r, c)]
	while que:
		r, c = que.pop()
		if data[r][c] != base:
			continue

		hist.append((r, c, data[r][c], color))
		data[r][c] = color
		for i in range(-1, 2, 2):
			if 0 <= r + i < 48:
				que.append((r + i, c))

		for i in range(-1, 2, 2):
			if 0 <= c + i < 64:
				que.append((r, c + i))

	if hist:
		global history, hi
		if len(history) > hi:
			history = history[:hi]
		hi += 1
		history.append(hist)

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
draw = False
fill = False
actual = 0
brush = 1
color = (0, 0, 0)
mouse = (0, 0)
showreal = False
try:
	while True:
		clock.tick(80) # FPS
		for event in pygame.event.get():
			if event.type == QUIT:
				raise KeyboardInterrupt()

			if event.type == MOUSEBUTTONDOWN:
				if event.button == 3:
					color = (255, 255, 255)

				elif event.button == 1:
					color = colors[actual]

				elif event.button == 5:
					actual = (actual + 1) % len(colors)
					continue

				elif event.button == 4:
					actual = (len(colors) + actual - 1) % len(colors)
					continue

				if fill:
					fillImage(event.pos, color)

				else:
					draw = True
					updateImage(event.pos, brush, color)

			if event.type == MOUSEBUTTONUP:
				draw = False
				color = colors[actual]

			if event.type == MOUSEMOTION:
				if draw:
					updateImage(event.pos, brush, color)

				mouse = event.pos

			if event.type == KEYDOWN:
				if event.key == K_1: actual = 0
				elif event.key == K_2: actual = 1
				elif event.key == K_3: actual = 2
				elif event.key == K_4: actual = 3
				elif event.key == K_5: actual = 4
				elif event.key == K_6: actual = 5
				elif event.key == K_7: actual = 6
				elif event.key == K_8: actual = 7
				elif event.key in (K_LSHIFT, K_RSHIFT): brush = 3
				elif event.key in (K_LSUPER, K_RSUPER): fill = True
				elif event.key == K_SPACE: showreal = not showreal
				elif event.key == K_z and event.mod & KMOD_CTRL and history and hi:
					print 'UNDO', hi, hi - 1
					actions = history[hi - 1]
					hi -= 1
					for x, y, color, _ in actions:
						data[x][y] = color

				elif event.key == K_y and event.mod & KMOD_CTRL and len(history) > hi:
					print 'REDO', hi, hi + 1
					actions = history[hi]
					hi += 1
					for x, y, _, color in actions:
						data[x][y] = color

			if event.type == KEYUP:
				if event.key in (K_LSHIFT, K_RSHIFT): brush = 1
				elif event.key in (K_LSUPER, K_RSUPER): fill = False

		if not draw:
			color = colors[actual]

		for r in range(48):
			for c in range(64):
				pygame.draw.rect(screen, data[r][c], (10 * c, 10 * r, 10, 10))

		c = mouse[0] / 10
		r = mouse[1] / 10
		for i in range(max(0, r - brush / 2), min(48, r + brush / 2 + 1)):
			for j in range(max(0, c - brush / 2), min(64, c + brush / 2 + 1)):
				pygame.draw.rect(screen, color, (10 * j, 10 * i, 10, 10))

		if showreal:
			for r in range(48):
				for c in range(64):
					pygame.draw.rect(screen, data[r][c], (576 + c, r, 2, 2))

		pygame.display.update()

except KeyboardInterrupt:
	pass

pickle.dump(data, open('image.dat', 'wb'))
