# -*- encoding: utf8 -*-

import pygame
from pygame.locals import *
from utils import *
from cursor import Cursor
import engine
from hub import Hub
import map
from map import Map
from ai import AI

class Pause(Exception): pass
class GameOver(Exception): pass
class GameWin(Exception): pass

class Scene(object):
	image = None
	def __init__(self, _engine):
		super(Scene, self).__init__()
		self._ais = []
		self._engine = _engine
		self._resx, self._resy = _engine.getResolution()
		self.surface = pygame.Surface((self._resx, self._resy))
		drawText(self.surface, "Wczytywanie mapy...", 48, (255, 255, 255), (self._resx / 2, self._resy / 2))
		self._map = Map(_engine)
		self._hub = Hub(_engine, self._map)
		self._cursor = Cursor(_engine, self._map)
		self._ais.append(AI(_engine, self._map, _engine.players[0], 0))
		self._ais.append(AI(_engine, self._map, _engine.players[1], 1))

	def screenUpdated(self):
		self._resx, self._resy = self._engine.getResolution()
		self.surface = pygame.transform.smoothscale(self.surface, (self._resx, self._resy))
		self._map.screenUpdated()
		self._hub.screenUpdated()
		self._cursor.screenUpdated()

	def show(self):
		try:
			while self._engine.tick():
				for event in pygame.event.get():
					if event.type == QUIT:
						self._engine.quit()

					elif event.type == KEYUP:
						if event.key == K_ESCAPE:
							raise Pause()

						elif event.key == K_TAB:
							for n, tank in enumerate(self._engine.players[0]['tanks']):
								if tank.focus:
									tank.setFocus(False)
									n = (n + 1) % len(self._engine.players[0]['tanks'])
									self._engine.players[0]['tanks'][n].setFocus(True)
									break

				if self._engine.state & engine.STATE_FAIL:
					self.surface.fill((0, 0, 0))
					drawText(self.surface, "Game Over", 50, (140, 0, 0), (self._resx / 2, self._resy / 2))
					self._engine.show(self.surface)
					continue

				if self._engine.state & engine.STATE_WIN:
					self.surface.fill((0, 0, 0))
					drawText(self.surface, "Gratulacje!", 50, (0, 140, 0), (self._resx / 2, self._resy / 2))
					self._engine.show(self.surface)
					continue

				if self._engine.timeLeft() == (0, 0):
					if self._engine.players[0]['score'] > self._engine.players[1]['score']:
						raise GameWin()

					raise GameOver()

				if not len(self._engine.players[0]['tanks']):
					raise GameOver()

				if not len(self._engine.players[1]['tanks']):
					raise GameWin()

				for tank in self._engine.players[0]['tanks']:
					if tank.focus: break

				else:
					self._engine.players[0]['tanks'][0].setFocus(True)

				keys = pygame.key.get_pressed()
				if keys[K_LEFT]:
					self._map.move(map.DIRECTION_LEFT)

				if keys[K_RIGHT]:
					self._map.move(map.DIRECTION_RIGHT)

				if keys[K_UP]:
					self._map.move(map.DIRECTION_UP)

				if keys[K_DOWN]:
					self._map.move(map.DIRECTION_DOWN)

				for ai in self._ais:
					ai.update()

				self._map.update()
				self._hub.update()
				self._cursor.update()
				self._map.draw(self.surface)
				self._hub.draw(self.surface)
				self._cursor.draw(self.surface)
				self._engine.show(self.surface)

		except Pause:
			self._engine.state ^= engine.STATE_GAME | engine.STATE_MENU

		except GameOver:
			self._engine.state |= engine.STATE_FAIL

		except GameWin:
			self._engine.state |= engine.STATE_WIN
