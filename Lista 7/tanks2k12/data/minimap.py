# -*- encoding: utf8 -*-

import pygame

class Minimap(object):
	def __init__(self, _engine, _map):
		super(Minimap, self).__init__()
		self._engine = _engine
		self._map = _map
		self.surface = pygame.transform.scale(self._map.surface, (256, 256))
		self.surface.set_alpha(128)
		self.players = pygame.Surface((256, 256))
		self.players.set_colorkey((0, 0, 0))
		self.frame = pygame.Surface((256, 256))
		self.frame.set_colorkey((0, 0, 0))
		self._mapsize = self._map.getSize()
		self.screenUpdated()

	def screenUpdated(self):
		self._res = self._engine.getResolution()
		self._window = (self._res[0] * 256 / self._mapsize[0], self._res[1] * 256 / self._mapsize[1])

	def update(self):
		self.players.fill((0, 0, 0))
		self.frame.fill((0, 0, 0))
		mw, mh = self._mapsize
		x, y = self._map.getPos()
		x, y = -x * 256 / mw, -y * 256 / mh
		pygame.draw.rect(self.frame, (255, 255, 255), (x, y, self._window[0], self._window[1]), 1)
		for i in (0, 1):
			for tank in self._engine.players[i]['tanks']:
				x, y = tank.getPos()
				x, y = x * 256 / mw, y * 256 / mh
				tw, th = 32 * 256 / mw, 32 * 256 / mh
				pygame.draw.rect(self.players, tank.focus and (255, 255, 255) or self._engine.players[i]['color'], (x, y, tw, th))

		for flag in self._map.flags:
			x, y = flag.getPos()
			x, y = x * 256 / mw, y * 256 / mh
			tw, th = 16 * 256 / mw, 16 * 256 / mh
			pygame.draw.rect(self.players, flag.getColor(), (x, y, tw, th))
			
	def draw(self, surface, pos):
		surface.blit(self.surface, pos)
		surface.blit(self.players, pos)
		surface.blit(self.frame, pos)
