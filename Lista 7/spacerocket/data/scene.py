# -*- encoding: utf8 -*-

import random
import pygame
from pygame.locals import *
from utils import *
import engine
from hub import Hub
import planet
from planet import Planet
from star import Star
from canister import Canister
from rocket import Rocket

class Pause(Exception): pass
class GameEnd(Exception): pass
class NextLevel(Exception): pass

class Scene(object):
	image = None
	def __init__(self, _engine):
		super(Scene, self).__init__()

		if not Scene.image:
			Scene.image = loadImage('data/gfx/background.png')

		self._engine = _engine
		self._resx, self._resy = _engine.getResolution()
		self._background = pygame.transform.smoothscale(self.image, (self._resx, self._resy))
		self.surface = self._background.copy()
		drawText(self.surface, "Poziom %d..." % self._engine.game['level'], 48, (255, 255, 255), (self._resx / 2, self._resy / 2))
		self._engine.show(self.surface)
		self._hub = Hub(_engine)
		self.planets = pygame.sprite.Group()
		self.rocket = pygame.sprite.GroupSingle()
		self.stars = pygame.sprite.Group()
		self.canisters = pygame.sprite.Group()
		self._first = True

	def screenUpdated(self):
		self._resx, self._resy = self._engine.getResolution()
		self._background = pygame.transform.smoothscale(self.image, (self._resx, self._resy))
		self.surface = pygame.transform.scale(self.surface, (self._resx, self._resy))
		self._hub.screenUpdated()

	def show(self):
		if self._first:
			self.surface = self._background.copy()
			drawText(self.surface, "Poziom %d(0%%)..." % self._engine.game['level'], 48, (255, 255, 255), (self._resx / 2, self._resy / 2))
			self._engine.show(self.surface)
			count = 0
			planets = random.randint(1, min(self._engine.game['level'] * 2, 8))
			stars = random.randint(self._engine.game['level'], self._engine.game['level'] * 5)
			canisters = random.randint(0, self._engine.game['level'])
			whole = (planets + stars + canisters + 1) * 0.01
			try:
				for _ in xrange(planets):
					self.planets.add(Planet(random.randint(planet.MIN_MASS, planet.MAX_MASS), randomPlace([p for p in self.planets], 100, (self._resx, self._resy))))
					count += 1
					self.surface = self._background.copy()
					drawText(self.surface, "Poziom %d(%d%%)..." % (self._engine.game['level'], count / whole), 48, (255, 255, 255), (self._resx / 2, self._resy / 2))
					self._engine.show(self.surface)

			except NoMore:
				pass

			try:
				for _ in xrange(stars):
					self.stars.add(Star(randomPlace([p for p in self.planets] + [s for s in self.stars], 16, (self._resx, self._resy))))
					count += 1
					self.surface = self._background.copy()
					drawText(self.surface, "Poziom %d(%d%%)..." % (self._engine.game['level'], count / whole), 48, (255, 255, 255), (self._resx / 2, self._resy / 2))
					self._engine.show(self.surface)

			except NoMore:
				pass

			try:
				for _ in xrange(canisters):
					self.canisters.add(Canister(randomPlace([p for p in self.planets] + [s for s in self.stars] + [c for c in self.canisters], 16, (self._resx, self._resy))))
					count += 1
					self.surface = self._background.copy()
					drawText(self.surface, "Poziom %d(%d%%)..." % (self._engine.game['level'], count / whole), 48, (255, 255, 255), (self._resx / 2, self._resy / 2))
					self._engine.show(self.surface)

			except NoMore:
				pass

			self.rocket.add(Rocket(self._engine, self, randomPlace([p for p in self.planets], 48, (self._resx, self._resy))))
			count += 1
			self.surface = self._background.copy()
			drawText(self.surface, "Poziom %d(%d%%)..." % (self._engine.game['level'], count / whole), 48, (255, 255, 255), (self._resx / 2, self._resy / 2))
			self._engine.show(self.surface)
			self._first = False

		try:
			while self._engine.tick():
				for event in pygame.event.get():
					if event.type == QUIT:
						self._engine.quit()

					if event.type == KEYUP and event.key == K_ESCAPE:
						raise Pause()

					if event.type == KEYUP and event.key == K_q:
						if self._engine.game['godmode']:
							self._engine.game['godmode'] = False
							self._engine.game['godlevel'] = self._engine.game['level']

				if self._engine.state & engine.STATE_END:
					self.surface.fill((0, 0, 0))
					drawText(self.surface, "Gratulacje! Twoj wynik: %d!" % self._engine.game['score'], 50, (0, 140, 0), (self._resx / 2, self._resy / 2))
					self._engine.show(self.surface)
					continue

				if len(self.stars) == 0:
					raise NextLevel()

				if self._engine.game['life'] <= 0 or not self._engine.game['fuel']:
					raise GameEnd()

				self.surface = self._background.copy()
				self.planets.update()
				self.stars.update()
				self.canisters.update()
				self.rocket.update()
				self._hub.update()
				self.planets.draw(self.surface)
				self.stars.draw(self.surface)
				self.canisters.draw(self.surface)
				self.rocket.draw(self.surface)
				self._hub.draw(self.surface)
				self._engine.show(self.surface)

		except Pause:
			self._engine.state ^= engine.STATE_GAME | engine.STATE_MENU

		except GameEnd:
			self._engine.state |= engine.STATE_END

		except NextLevel:
			self._engine.nextLevel()
