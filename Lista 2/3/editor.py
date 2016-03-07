# -*- encoding: utf8 -*-
import sys
import os
import pygame
from pygame.locals import *
from utils import *

def inRectangle(point, A, B):
	return A[0] <= point[0] < B[0] and A[1] <= point[1] < B[1]

class EditorMenu:
	"""Menu of level editor."""

	def __init__(self, screen, tiles):
		self.screen = screen
		self.tiles = tiles
		self.background = loadImage('data/gfx/menu/background.png', None, True)
		self.actual = None
		self.hover = None
		self.state = [
		    loadImage('data/gfx/menu/normal.png', None, True),
		    loadImage('data/gfx/menu/active.png', None, True),
		]

	def update(self, events):
		for event in events:
			if not self.actual and event.type == MOUSEBUTTONDOWN:
				pos = list(event.pos)
				pos[0] = (pos[0] - 609) / 38
				pos[1] = (pos[1] - 40) / 38
				if pos[0] >= 0 and pos[1] >= 0:
					self.actual = str(pos[1] * 5 + pos[0] + 1)

			if event.type == MOUSEBUTTONUP:
				self.actual = None

			if event.type == MOUSEMOTION:
				self.hover = None
				pos = list(event.pos)
				pos[0] = (pos[0] - 609) / 38
				pos[1] = (pos[1] - 40) / 38
				if pos[0] >= 0 and pos[1] >= 0:
					self.hover = str(pos[1] * 5 + pos[0] + 1)

		self.screen.blit(self.background, (0, 0))
		for r in range(5):
			for c in range(5):
				tile = str(r * 5 + c + 1)
				self.screen.blit(self.tiles[tile], (609 + c * 38, 40 + r * 38))
				self.screen.blit(self.state[tile in (self.actual, self.hover)], (606 + c * 38, 37 + r * 38))

class Editor:
	"""Level editor."""

	SIZE = 20

	def __init__(self, resolution = (800, 600)):
		"""Initialize editor."""

		pygame.init()
		self.screen = pygame.display.set_mode(resolution)
		pygame.display.set_caption('Level editor')
		self.screen.blit(loadImage('data/gfx/background.png'), (0, 0))
		self.tiles = loadImages('data/gfx/tiles/')
		self.clock = pygame.time.Clock()
		self.menu = EditorMenu(self.screen, self.tiles)
		try:
			self.map = list(map(lambda x: x.split(), open('map.dat', 'r').read().split("\n")))
			if len(self.map) != self.SIZE:
				raise Exception()

			for r in range(self.SIZE):
				if len(self.map[r]) != self.SIZE:
					raise Exception()

		except Exception, msg:
			print 'WARNING:', msg
			self.map = [['1'] * self.SIZE for _ in range(self.SIZE)]

	def update(self):
		"""Update screen."""

		self.clock.tick(80)
		events = pygame.event.get()
		mouse = pygame.mouse.get_pos()
		for event in events:
			if event.type == QUIT:
				return False

			if self.menu.actual and event.type == MOUSEBUTTONUP:
				pos = list(event.pos)
				pos[0] = pos[0] / 30
				pos[1] = pos[1] / 30
				if 0 <= pos[0] <= self.SIZE and 0 <= pos[1] <= self.SIZE:
					self.map[pos[1]][pos[0]] = self.menu.actual

		# DRAW MENU
		self.menu.update(events)

		# DRAW TILES
		for r in range(self.SIZE):
			for c in range(self.SIZE):
				if self.menu.actual and inRectangle(mouse, (c * 30, r * 30), (30 + c * 30, 30 + r * 30)):
					tile = self.menu.actual
				else:
					tile = self.map[r][c]

				self.screen.blit(self.tiles[tile], (c * 30, r * 30))

		# DRAW CURSOR
		if self.menu.actual:
			self.screen.blit(self.tiles[self.menu.actual], (mouse[0] - 15, mouse[1] - 15))

		# UPDATE DISPLAY
		pygame.display.update()
		return True

	def save(self):
		data = open('map.dat', 'w')
		data.write("\n".join([' '.join(row) for row in self.map]))
		data.close()

if __name__ == '__main__':
	editor = Editor()
	try:
		while editor.update():
			pass

		editor.save()

	except KeyboardInterrupt:
		sys.exit(0)

