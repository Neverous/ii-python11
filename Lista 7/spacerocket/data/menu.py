# -*- encoding: utf8 -*-

import pygame
from pygame.locals import *
from utils import *
import engine

class MenuExit(Exception): pass
class NewGame(Exception): pass
class ContinueGame(Exception): pass

class MenuElement(object):
	def __init__(self, textfunc, activefunc = lambda: True, callback = lambda: True):
		super(MenuElement, self).__init__()
		self.text = textfunc
		self.active = activefunc
		self.callback = callback

class Menu(object):
	image = None
	def __init__(self, _engine):
		super(Menu, self).__init__()
		if not Menu.image:
			Menu.image = loadImage('data/gfx/menu.png')

		self._engine = _engine
		self._resx, self._resy = _engine.getResolution()
		self._background = pygame.transform.smoothscale(self.image, _engine.getResolution())
		self.surface = self._background.copy()
		self._focus = 0
		self._loaded = 255
		self._step = 15
		self._buttons = [
			MenuElement(lambda: "Nowa Gra", lambda: True, lambda: raise_(NewGame())),
			MenuElement(lambda: "Kontynuuj", lambda: _engine.state & engine.STATE_PLAY, lambda: raise_(ContinueGame())),
			MenuElement(lambda: _engine.getFullscreen() and "Okno" or "Pelny Ekran", lambda: True, lambda: _engine.toggleFullscreen()),
			MenuElement(lambda: "Rozdzielczosc: %dx%d" % _engine.getResolution(), lambda: not _engine.state & engine.STATE_PLAY, lambda: _engine.toggleResolution()),
			MenuElement(lambda: "Wyjdz", lambda: True, lambda: _engine.quit()),
		]

	def screenUpdated(self):
		self._resx, self._resy = self._engine.getResolution()
		self._background = pygame.transform.smoothscale(self.image, (self._resx, self._resy))
		self.surface = pygame.transform.smoothscale(self.surface, (self._resx, self._resy))

	def fadein(self):
		while self._loaded < 255 and self._engine.tick():
			self._loaded += self._step
			self.surface.set_alpha(self._loaded)
			self._engine.show(self.surface)

	def fadeout(self):
		while self._loaded > 0 and self._engine.tick():
			self._loaded -= self._step
			self.surface.set_alpha(self._loaded)
			temp = pygame.Surface((self._resx, self._resy))
			temp.blit(self._engine.scene.surface, (0, 0))
			temp.blit(self.surface, (0, 0))
			self._engine.show(temp)

	def show(self):
		self.fadein()
		try:
			while self._engine.tick():
				for event in pygame.event.get():
					if event.type == QUIT:
						self._engine.quit()

					if event.type == KEYUP:
						if event.key == K_ESCAPE:
							if self._engine.state & engine.STATE_STOP:
								self._focus = len(self._buttons) - 1

							if self._engine.state & engine.STATE_PLAY:
								raise ContinueGame()

						elif event.key in (K_DOWN, K_UP):
							step = event.key == K_DOWN and 1 or -1
							self._focus = (self._focus + step) % len(self._buttons)
							while not self._buttons[self._focus].active():
								self._focus = (self._focus + step) % len(self._buttons)

						elif event.key == K_RETURN:
							self._buttons[self._focus].callback()

				self.surface.blit(self._background, (0, 0))
				# Draw "buttons"
				shift = 300
				for n, button in enumerate(self._buttons):
					_, height = drawText(self.surface, button.text(), 14, (self._focus == n and (255, 0, 0)) or (button.active() and (255, 255, 255)) or (128, 128, 128), (self._resx / 2, shift))
					shift += height + 20

				self._engine.show(self.surface)

		except ContinueGame:
			self._engine.state ^= engine.STATE_GAME | engine.STATE_MENU

		except NewGame:
			self._engine.newGame()
			self._engine.state = engine.STATE_GAME | engine.STATE_PLAY

		self.fadeout()
