# -*- encoding: utf8 -*-
# Maciej Szeptuch 2012

from collections import defaultdict
import pygame
from pygame.locals import *
from map import HoverLayer
import utils
import field
import wall
import stairs
import trap
import chest

class TilesGrid(object):
	"""Menu wyboru "kafelków" w edytorze."""

	def __init__(self, _engine, _editor, _map):
		"""_engine - obiekt silnika, _editor - obiekt edytora, _map - obiekt mapy."""

		super(TilesGrid, self).__init__()
		self.images = {
			'hover': utils.loadImage('data/gfx/hover.png', alpha = True),
			'normal': utils.loadImage('data/gfx/normal.png', alpha = True),
		}

		self._engine = _engine
		self._editor = _editor
		self._map = _map
		self._layer = HoverLayer(_map, True)
		self._map.addLayer('ToolHover', 5, self._layer)
		self._clicked = None
		self._hover = None
		self._updated = []
		self.screenUpdated()
		self.surface = pygame.Surface((192, 312))
		self.surface.fill((1, 5, 4))
		self.surface.set_colorkey((1, 5, 4))
		self._tool = Tool(_editor, _map)
		self._toolHover = HoverLayer.Sprite()
		self._layer.add('tool', self._toolHover)
		_tiles = ( # dostępne kafelki
			field.Field,
			wall.WallTopLeft, wall.WallTopRight, wall.WallBottomLeft, wall.WallBottomRight, wall.WallHorizontal, wall.WallVertical,
			stairs.StairsUpNorth, stairs.StairsDownNorth, stairs.StairsUpSouth, stairs.StairsDownSouth, stairs.StairsUpWest, stairs.StairsDownWest, stairs.StairsUpEast, stairs.StairsDownEast,
			trap.TrapMoveArrow, trap.TrapMoveFire, trap.TrapMoveIce, trap.TrapTouchArrow, trap.TrapTouchFire, trap.TrapTouchIce,
			chest.ChestNorth, chest.ChestSouth, chest.ChestWest, chest.ChestEast,
		)

		_modifiers = (field.MODIFIER_HERO, field.MODIFIER_SPIDER, field.MODIFIER_SKELETON, field.MODIFIER_MAGE, field.MODIFIER_TROLL)

		# Kafelki
		utils.drawText(self.surface, "Kafelki", 22, (255, 255, 255), (96, 10))
		self._tiles = pygame.sprite.Group()
		for y in xrange(5):
			for x in xrange(5):
				tile = _tiles[y * 5 + x]
				tile = tile.Sprite((x, y), tile)
				tile.rect.center = tile.rect.centerx + x * 8, tile.rect.centery + y * 8 + 20
				self._tiles.add(tile)

		self._tiles.draw(self.surface)
		for tile in self._tiles:
			self.surface.blit(self.images['hover'], tile.rect.topleft)
			self.surface.blit(self.images['normal'], tile.rect.topleft)

		# Modyfikatory
		utils.drawText(self.surface, "Modyfikatory", 22, (255, 255, 255), (96, 225))
		self._modifiers = pygame.sprite.Group()
		for x in xrange(5):
			modifier = field.Modifier((x, 0), _modifiers[x])
			modifier.rect.center = modifier.rect.centerx + x * 8, modifier.rect.centery + 240
			self._modifiers.add(modifier)

		self._modifiers.draw(self.surface)
		for tile in self._modifiers:
			self.surface.blit(self.images['hover'], tile.rect.topleft)
			self.surface.blit(self.images['normal'], tile.rect.topleft)

	def getRectangle(self):
		"""Zwraca obszar zajmowany przez menu."""

		return pygame.Rect(self._pos[0], self._pos[1], 192, 280)

	def screenUpdated(self):
		"""Aktualizuje pozycję menu i wymusza odświeżenie obszaru."""

		self._resx, self._resy = self._engine.getResolution()
		_resx = self._resx
		self._resx = int((self._resx - 200) / 32) * 32
		_pad = (_resx - self._resx - 192) / 2
		self._pos = (self._resx + _pad, 2 * _pad + 192)
		self._refresh = True

	def update(self):
		"""Aktualizowanie klikniętych kafelków/modyfikatorów."""

		updated = [(x + self._pos[0], y + self._pos[1], w, h) for x, y, w, h in self._updated]
		self._updated = []
		if self._refresh:
			self._refresh = False
			return [(self._pos[0], self._pos[1], 192, 280)]

		return updated

	def draw(self, surface):
		"""Rysuje menu na powierzchni."""

		surface.blit(self.surface, (self._pos[0], self._pos[1]))

	def mouseEvent(self, _event, _pos = None):
		"""Obsługa zdarzeń myszy."""

		if not _pos:
			if self._hover:
				if self._hover and self._hover != self._clicked:
					x, y, w, h = self._hover.rect
					self.surface.blit(self.images['normal'], (x, y))
					self._updated.append((x, y, w, h))

				self._hover = None

			if self._map.getRectangle().collidepoint(_event.pos):
				if _event.type == MOUSEBUTTONDOWN and _event.button == 1:
					self._tool.use(_event.pos)

				if _event.type == MOUSEMOTION:
					self._layer.move('tool', _event.pos)

			return

		self._layer.clear('tool')
		if _event.type == MOUSEBUTTONDOWN and _event.button == 1:
			if self._clicked:
				x, y, w, h = self._clicked.rect
				self.surface.blit(self.images['normal'], (x, y))
				self._updated.append((x, y, w, h))

			for tile in self._tiles:
				if tile.rect.collidepoint(_pos):
					self._clicked = tile
					x, y, w, h = self._clicked.rect
					self.surface.blit(self.images['hover'], (x, y))
					self._updated.append((x, y, w, h))
					self._tool = ToolSetFieldType(self._editor, self._map, tile.getLogic())
					_img = tile.image.copy()
					pygame.draw.rect(_img, (255, 255, 255), (0, 0, 32, 32), 1)
					_img.set_alpha(128)
					self._toolHover.changeImage(_img)
					return

			for modifier in self._modifiers:
				if modifier.rect.collidepoint(_pos):
					self._clicked = modifier
					x, y, w, h = self._clicked.rect
					self.surface.blit(self.images['hover'], (x, y))
					self._updated.append((x, y, w, h))
					self._tool = ToolToggleModifier(self._editor, self._map, modifier.getModifier())
					_img = modifier.image.copy()
					pygame.draw.rect(_img, (255, 255, 255), (0, 0, 32, 32), 1)
					_img.set_alpha(128)
					self._toolHover.changeImage(_img)
					return

			self._clicked = None
			self._tool = Tool(self._editor, self._map)
			self._toolHover.changeImage(pygame.Surface((0, 0)))
			return

		if _event.type == MOUSEMOTION:
			_hover = None
			for tile in self._tiles:
				if tile.rect.collidepoint(_pos):
					_hover = tile
					break

			if not _hover:
				for modifier in self._modifiers:
					if modifier.rect.collidepoint(_pos):
						_hover = modifier
						break

			if self._hover == _hover:
				return

			if self._hover and self._hover != self._clicked:
				x, y, w, h = self._hover.rect
				self.surface.blit(self.images['normal'], (x, y))
				self._updated.append((x, y, w, h))

			self._hover = _hover
			if self._hover:
				x, y, w, h = self._hover.rect
				self.surface.blit(self.images['hover'], (x, y))
				self._updated.append((x, y, w, h))

class Tool(object):
	"""Reprezentacja wybranego narzędzia."""

	def __init__(self, _editor, _map):
		"""_editor - obiekt edytora, _map - obiekt mapy, _image - obrazek narzędzia."""

		super(Tool, self).__init__()
		self._map = _map
		self._editor = _editor

	def use(self, _pos):
		"""Użycie narzędzia w miejscu _pos."""

		pass

class ToolSetFieldType(Tool):
	"""Narzędzie zmiany pola."""

	def __init__(self, _editor, _map, _type):
		"""_editor - obiekt edytora, _map - obiekt mapy, _type - typ pola."""

		super(ToolSetFieldType, self).__init__(_editor, _map)
		self._type = _type

	def use(self, _pos):
		"""Ustawia pole w pozycji _pos na dany."""

		if not self._map.getLayer('Fields').get(_pos, True): return

		_x, _y = self._map.getLayer('Fields').get(_pos, True).getGrid()
		self._editor.setField(self._map.getStorey(), _x, _y, self._type((_x, _y)))

class ToolToggleModifier(Tool):
	"""Narzędzie zmiany modyfikatora."""

	def __init__(self, _editor, _map, _modifier):
		"""_editor - obiekt edytora, _map - obiekt mapy, _modifier - modyfikator."""

		super(ToolToggleModifier, self).__init__(_editor, _map)
		self._modifier = _modifier

	def use(self, _pos):
		"""Ustawia modyfikator polu w pozycji _pos."""

		_field = self._map.getLayer('Fields').get(_pos, True)
		if not _field: return

		_field.getLogic().setModifier(self._modifier)
