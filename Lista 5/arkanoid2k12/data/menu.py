# -*- encoding: utf-8 -*-
import pygame
from pygame.locals import *
from utils import *
import engine

class MenuOut(Exception): pass

class Button(object):
	def __init__(self, engine, text, textfunc = None, activefunc = None, callback = lambda _: True):
		super(Button, self).__init__()
		self.txt = text
		self.engine = engine
		self.callback = callback
		if textfunc: self.text = textfunc
		if activefunc: self.active = activefunc

	def text(self): return self.txt
	def active(self): return True

class Menu(object):
	image = None
	sounds = None
	def __init__(self, Engine):
		super(Menu, self).__init__()
		self.engine = Engine
		self.loaded = 100
		if not Menu.image:
			Menu.image = loadImage('data/gfx/menu.jpg')

		self.background = pygame.transform.smoothscale(self.image, self.engine.getResolution())
		self.surface = self.background.copy()
		if not Menu.sounds:
			Menu.sounds = defaultdict(lambda: NoSound(), {
				'over': loadSound('data/snd/menuover.wav'),
				'background': loadSound('data/snd/menubackground.wav'),
			})

		self.buttons = [
			Button(self.engine, "Nowa gra", callback = self.newGame),
			Button(self.engine, "Kontynuuj",
				activefunc = lambda: self.engine.state & engine.STATE_PLAY,
				callback = self.continueGame),
			Button(self.engine, "Sterowanie",
				lambda: "Sterowanie: %s" % (self.engine.getControls() & engine.CONTROLS_KEYBOARD and "Klawiatura" or "Mysz"),
				callback = self.engine.toggleControls),
			Button(self.engine, "Pelny Ekran",
				callback = self.engine.toggleFullscreen),
			Button(self.engine, "Rozdzielczosc",
				lambda: "Rozdzielczosc: %dx%d" % self.engine.getResolution(),
				lambda: self.engine.state & engine.STATE_STOP,
				callback = self.engine.toggleResolution),
			Button(self.engine, "Wyjdz", callback = self.exit),
		]

		self.focus = 0

	def newGame(self):
		self.engine.newGame()
		self.engine.state = engine.STATE_PLAY | engine.STATE_MENU
		self.continueGame()

	def continueGame(self):
		raise MenuOut()

	def exit(self):
		raise KeyboardInterrupt()

	def show(self):
		self.sounds['background'].play(-1)
		self.slide(2)
		try:
			while True:
				self.engine.tick()
				for event in pygame.event.get():
					if event.type == QUIT:
						raise KeyboardInterrupt()

					if event.type == KEYUP:
						self.sounds['over'].play()
						if event.key == K_ESCAPE and self.engine.state & engine.STATE_PLAY:
							raise MenuOut()

						elif event.key == K_DOWN:
							self.focus = (self.focus + 1) % len(self.buttons)
							while not self.buttons[self.focus].active():
								self.focus = (self.focus + 1) % len(self.buttons)

						elif event.key == K_UP:
							self.focus = (self.focus - 1) % len(self.buttons)
							while not self.buttons[self.focus].active():
								self.focus = (self.focus - 1) % len(self.buttons)

						elif event.key == K_RETURN:
							self.buttons[self.focus].callback()

				self.surface.blit(self.background, (0, 0))
				resx, resy = self.engine.getResolution()

				# Draw Title
				self.engine.writeText(self.surface, "Arkanoid 2k12", 32, (255, 255, 255), (resx / 2, 100))

				# Draw "buttons"
				shift = 350
				for n, button in enumerate(self.buttons):
					_, height = self.engine.writeText(self.surface, button.text(), 14, (self.focus == n and (255, 0, 0)) or (button.active() and (255, 255, 255)) or (128, 128, 128), (resx / 2, shift))
					shift += height + 20

				# Draw all to screen
				self.engine.screen.blit(self.surface, (0, 0))
				pygame.display.update()

		except MenuOut:
			self.engine.state ^= engine.STATE_GAME | engine.STATE_MENU

		self.slide(-2)
		self.sounds['background'].fadeout(1500)

	def slide(self, step):
		res = self.engine.getResolution()[1]
		while (step > 0 and self.loaded < 100) or (step < 0 and self.loaded > 0):
			self.engine.tick()
			self.loaded += step
			if step < 0:
				self.engine.screen.blit(self.engine.scene.surface, (0, 0))

			self.engine.screen.blit(self.surface, (0, res - res * self.loaded / 100))
			pygame.display.update()

	def screenUpdated(self):
		self.background = pygame.transform.smoothscale(self.image, self.engine.getResolution())
		self.surface = pygame.transform.smoothscale(self.surface, self.engine.getResolution())


