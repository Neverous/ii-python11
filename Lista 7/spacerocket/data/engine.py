# -*- encoding: utf8 -*-

from collections import defaultdict
import time
import pygame
from pygame.locals import *
from utils import *
from menu import Menu
from scene import Scene
import rocket

# Game states
STATE_STOP = 1
STATE_PLAY = 2
STATE_END  = 4
STATE_GAME = 8
STATE_MENU = 16

class Engine(object):
	def __init__(self, debug = False):
		super(Engine, self).__init__()
		self.options = defaultdict(lambda: '', {
			'resolution':0,
			'resolutions': tuple(reversed(filter(lambda (x, y): y >= 600, pygame.display.list_modes()))),
			'fullscreen': 0,
			'fps': 30,
		})
		self.game = defaultdict(lambda: '', {
			'level': 1,
			'score': 0,
			'life': 4,
			'godmode': True,
			'godlevel': 0,
			'fuel': rocket.MAX_FUEL,
		})
		self.screen = pygame.display.set_mode(self.getResolution())
		self.clock = pygame.time.Clock()
		self.state = STATE_STOP | STATE_MENU
		self.menu = Menu(self)
		self.scene = None

	def quit(self):
		raise KeyboardInterrupt()

	def tick(self):
		if self.getFPS():
			self.clock.tick(self.getFPS())

		return True

	def _updateScreen(self):
		self.screen = pygame.display.set_mode(self.getResolution(), (self.getFullscreen() and pygame.FULLSCREEN))
		self.menu.screenUpdated()
		if self.scene:
			self.scene.screenUpdated()

	def newGame(self):
		self.game = defaultdict(lambda: '', {
			'level': 1,
			'score': 0,
			'life': 4,
			'godmode': True,
			'godlevel': 0,
			'fuel': rocket.MAX_FUEL,
		})
		self.scene = Scene(self)

	def nextLevel(self):
		self.game['level'] += 1
		self.scene = Scene(self)

	def toggleResolution(self):
		self.options['resolution'] += 1
		self.options['resolution'] %= len(self.options['resolutions'])
		self._updateScreen()

	def getResolution(self):
		return self.options['resolutions'][self.options['resolution']]

	def toggleFullscreen(self):
		self.options['fullscreen'] ^= 1
		self._updateScreen()

	def getFullscreen(self):
		return self.options['fullscreen']

	def setFPS(self, fps):
		self.options['fps'] = fps

	def getFPS(self):
		return self.options['fps']

	def show(self, surface):
		self.screen.blit(surface, (0, 0))
		pygame.display.update()

	def run(self):
		try:
			while True:
				if self.state & STATE_MENU:
					self.menu.show()

				elif self.state & STATE_GAME:
					self.scene.show()

		except KeyboardInterrupt:
			pass
