# -*- encoding: utf8 -*-

from collections import defaultdict
import time
import pygame
from pygame.locals import *
from utils import *
from menu import Menu
from scene import Scene

# Game states
STATE_STOP = 1
STATE_PLAY = 2
STATE_WIN  = 4
STATE_FAIL = 8
STATE_GAME = 16
STATE_MENU = 32

class Engine(object):
	def __init__(self, debug = False):
		super(Engine, self).__init__()
		self.options = defaultdict(lambda: '', {
			'resolution':0,
			'resolutions': tuple(reversed(filter(lambda (x, y): y >= 600 and x >= 1024, pygame.display.list_modes()))),
			'fullscreen': 0,
			'fps': 30,
			'debug': debug,
		})
		self.players = [
			defaultdict(lambda: '', {
				'id': 0,
				'score': 0,
				'tanks': [],
				'color': (0, 255, 255),
			}),
			defaultdict(lambda: '', {
				'id': 1,
				'score': 0,
				'tanks': [],
				'color': (255, 0, 0),
			}),
		]
		self.game = defaultdict(lambda: '', {
			'end': 300,
			'lastcheck': time.time(),
			'level': 'basic',
		})
		self.levels = loadLevels('data/maps/')
		self.screen = pygame.display.set_mode(self.getResolution())
		self.clock = pygame.time.Clock()
		self.state = STATE_STOP | STATE_MENU
		self.menu = Menu(self)
		self.scene = None

	def getLevel(self):
		return self.levels[self.game['level']]

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
		self.players = [
			defaultdict(lambda: '', {
				'id': 0,
				'score': 0,
				'tanks': [],
				'color': (0, 255, 255),
			}),
			defaultdict(lambda: '', {
				'id': 1,
				'score': 0,
				'tanks': [],
				'color': (255, 0, 0),
			}),
		]
		self.game = defaultdict(lambda: '', {
			'end': 300,
			'lastcheck': time.time(),
			'level': 'basic',
		})
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

	def timeLeft(self):
		temp = time.time()
		if self.state & STATE_PLAY:
			self.game['end'] = max(self.game['end'] - temp + self.game['lastcheck'], 0)

		self.game['lastcheck'] = temp
		return (self.game['end'] / 60, self.game['end'] % 60)

	def run(self):
		try:
			while True:
				self.game['lastcheck'] = time.time()
				if self.state & STATE_MENU:
					self.menu.show()

				elif self.state & STATE_GAME:
					self.scene.show()

		except KeyboardInterrupt:
			pass
