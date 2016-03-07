# -*- encoding: utf-8 -*-
from collections import defaultdict
import time
import threading
import pygame
from pygame.locals import *
from utils import *
from menu import Menu
from scene import Scene
# Game states
STATE_STOP  = 1
STATE_PLAY  = 2
STATE_FAIL  = 4
STATE_WIN   = 8
STATE_GAME  = 16
STATE_MENU  = 32

# Control methods
CONTROLS_KEYBOARD   = 1
CONTROLS_MOUSE      = 2

class Engine(object):
	def __init__(self):
		super(Engine, self).__init__()
		self.options = defaultdict(lambda: '', {
			'resolution': 0,
			'resolutions': tuple(reversed(filter(lambda (x, y): y >= 600, pygame.display.list_modes()))),
			'fullscreen': False,
			'fps': 60,
			'controls': CONTROLS_KEYBOARD,
		})
		self.screen = pygame.display.set_mode(self.getResolution(), (self.getFullscreen() and pygame.FULLSCREEN))
		pygame.mouse.set_visible(False)
		self.level = loadLevels('data/levels')
		self.newGame()
		self.state = STATE_STOP | STATE_MENU
		self.menu = Menu(self)
		self.updateScreen()
		self.timer = pygame.time.Clock()
		self.fonts = {}

	def writeText(self, surface, text, size, color, (x, y), antialiasing = True):
		if not size in self.fonts:
			self.fonts[size] = pygame.font.Font(pygame.font.get_default_font(), size)

		render = self.fonts[size].render(text, antialiasing, color)
		width, height = render.get_size()
		surface.blit(render, (x - width / 2, y - height / 2))
		return width, height

	def newGame(self):
		self.player = defaultdict(lambda: '', {
			'level': 0,
			'score': 0,
			'lives': 3,
		})
		self.nextLevel()

	def tick(self):
		if self.getFPS():
			self.timer.tick(self.getFPS())

	def run(self):
		try:
			self.screen.blit(self.scene.surface, (0, 0))
			while True:
				if self.state & STATE_MENU:
					self.menu.show()

				elif self.state & STATE_GAME:
					self.scene.show()

		except KeyboardInterrupt:
			pass

	def updateScreen(self):
		self.screen = pygame.display.set_mode(self.getResolution(), (self.getFullscreen() and pygame.FULLSCREEN))
		self.menu.screenUpdated()
		self.scene.screenUpdated()

	def toggleResolution(self):
		self.options['resolution'] += 1
		self.options['resolution'] %= len(self.options['resolutions'])
		self.updateScreen()

	def getResolution(self):
		return self.options['resolutions'][self.options['resolution']]

	def toggleFullscreen(self):
		self.options['fullscreen'] = not self.options['fullscreen']
		self.updateScreen()

	def getFullscreen(self):
		return self.options['fullscreen']

	def getControls(self):
		return self.options['controls']

	def toggleControls(self):
		self.options['controls'] ^= CONTROLS_KEYBOARD | CONTROLS_MOUSE
		pygame.event.set_grab(self.options['controls'] & CONTROLS_MOUSE)

	def nextLevel(self):
		self.player['level'] += 1
		if self.player['level'] in self.level:
			self.player['bonuses'] = []
			self.scene = Scene(self, self.level[self.player['level']])
			return True

		return False

	def getFPS(self):
		return self.options['fps']

	def setFPS(self, fps):
		self.options['fps'] = fps
