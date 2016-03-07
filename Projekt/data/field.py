# -*- encoding: utf8 -*-
# Maciej Szeptuch 2012

import pygame
import utils

## MODYFIKATORY

MODIFIER_BLOCKED	= 1		# Pole zablokowane
MODIFIER_HERO		= 2		# Pole spawnu bohatera
MODIFIER_SPIDER		= 4		# Pole spawnu pająka
MODIFIER_SKELETON	= 8		# Pole spawnu szkieleta
MODIFIER_MAGE		= 16	# Pole spawnu maga
MODIFIER_TROLL		= 32	# Pole spawnu trola
MODIFIER_ITEM		= 64	# Przedmioty na polu

class Modifier(pygame.sprite.Sprite):
	"""Graficzna reprezentacja modyfikatora pola."""

	def __init__(self, _grid, _modifier):
		"""_grid - pozycja pola na siatce, _modifier - modyfikator."""

		super(Modifier, self).__init__()
		self.images = {
			MODIFIER_HERO: utils.loadImage('data/gfx/hero/sign.png', alpha = True),
			MODIFIER_SPIDER: utils.loadImage('data/gfx/spider/sign.png', alpha = True),
			MODIFIER_SKELETON: utils.loadImage('data/gfx/skeleton/sign.png', alpha = True),
			MODIFIER_MAGE: utils.loadImage('data/gfx/mage/sign.png', alpha = True),
			MODIFIER_TROLL: utils.loadImage('data/gfx/troll/sign.png', alpha = True),
			MODIFIER_ITEM: utils.loadImage('data/gfx/sack.png', alpha = True),
		}

		self._grid = _grid
		self._pos = _grid[0] * 32 + 16, _grid[1] * 32 + 16
		self._modifier = _modifier
		self.image = self.images[_modifier]
		self.rect = self.image.get_rect()
		self.rect.center = _grid[0] * 32 + 16, _grid[1] * 32 + 16

	def getGrid(self):
		"""Zwraca pozycje pola na siatce."""

		return self._grid

	def getModifier(self):
		"""Zwraca obsługiwany modyfikator."""

		return self._modifier

	def update(self):
		"""Nic nie trzeba robić. Zwraca pustą listę."""

		return []

	def draw(self, surface):
		"""Rysuje reprezentacje modyfikatora na danej powierzchni."""

		surface.blit(self.image, self.rect.topleft)

class Field(object):
	"""Logika pustego pola."""

	def __init__(self, _grid):
		"""_grid - pozycja na siatce."""

		super(Field, self).__init__()
		self._grid = _grid
		self._modifier = 0
		self._occupy = None		# Potwór/Bohater znajdujący się na polu
		self._items = []		# Przedmioty znajdujące się na polu
		self._refresh = False

	def getGrid(self):
		"""Zwraca pozycje pola na siatce."""

		return self._grid

	def getSprite(self, _showModifiers = False):
		"""Zwraca reprezentacje graficzną pola. UWAGA: za każdym wywołaniem tworzy nowy obiekt!
	_showModifiers - czy rysować reprezentacje modyfikatora."""

		return self.Sprite(self._grid, self, _showModifiers = _showModifiers)

	def setModifier(self, _modifier):
		"""Ustawia modyfikator pola. Jeśli podany jest taki sam jak aktualny modyfikator zostaje usunięty."""

		self._refresh = True
		if self._modifier == _modifier:
			self._modifier = 0
			return

		self._modifier = _modifier

	def getModifier(self):
		"""Zwraca modyfikator pola."""

		return self._modifier

	def getOccupied(self):
		"""Zwraca stworzenie zajmujące pole."""

		return self._occupy

	def getItems(self):
		"""Zwraca przedmioty z pola."""

		return self._items

	def occupy(self, _creature):
		"""Zajmuje pole."""

		self._occupy = _creature

	def update(self):
		"""Sprawdza wskaźnik na zajmująca jednostke i w razie potrzeby poprawia go."""

		if self._occupy and not self._occupy.getLife():
			self._occupy = None

		self._items = list(filter(lambda _item: _item.getAttached() == self, self._items))
		if self._refresh:
			self._refresh = False
			return True

		return False

	def clicked(self, _scene, _hero):
		"""Akcja wywoływana gdy naciśnie się na pole.
	_scene - aktualna scena."""

		if utils.distance(_hero.getGrid()[:2], self._grid[:2]) > 1:
			return

		while self._items and len(_hero.inventory) < 15:
			_scene.inventory.add(self._items.pop())

		self._refresh = True

	def entered(self, _creature):
		"""Akcja wywoływana gdy stwór wejdzie na pole.
	_scene - aktualna scena,
	_creature - rzeczony stwór."""

		pass

	def putItem(self, _item):
		"""Akcja wywoływana gdy przedmiot zostanie odłożony na pole. Zwraca fałsz jeśli niemożliwe
	_scene - aktualna scena,
	_item - odłożony przedmiot."""

		self._items.append(_item)
		self._refresh = True
		return True

	class Sprite(pygame.sprite.Sprite):
		"""Graficzna reprezentacja pustego pola."""

		def __init__(self, _grid, _logic, _image = 'data/gfx/field.png', _showModifiers = False):
			"""_grid - pozycja na siatce, _logic - logika pola, _image - scieżka do obrazka, _showModifiers - czy rysować reprezentacje modyfikatora."""

			super(Field.Sprite, self).__init__()
			self.image = utils.loadImage(_image)
			self.modifiers = {
				MODIFIER_HERO: utils.loadImage('data/gfx/hero/sign.png', alpha = True),
				MODIFIER_SPIDER: utils.loadImage('data/gfx/spider/sign.png', alpha = True),
				MODIFIER_SKELETON: utils.loadImage('data/gfx/skeleton/sign.png', alpha = True),
				MODIFIER_MAGE: utils.loadImage('data/gfx/mage/sign.png', alpha = True),
				MODIFIER_TROLL: utils.loadImage('data/gfx/troll/sign.png', alpha = True),
				MODIFIER_BLOCKED: None,
				MODIFIER_ITEM: utils.loadImage('data/gfx/sack.png', alpha = True),
			}

			self._logic = _logic
			self._grid = _grid
			self._showModifiers = _showModifiers
			self._refresh = True
			self.rect = self.image.get_rect()
			self.rect.center = _grid[0] * 32 + 16, _grid[1] * 32 + 16

		def getGrid(self):
			"""Zwraca pozycje pola na siatce."""

			return self._grid

		def getLogic(self):
			"""Zwraca obiekt logiki powiązany z polem."""

			return self._logic

		def update(self):
			"""Aktualizuje pole."""

			if self._logic.update() or self._refresh:
				self._refresh = False
				return [list(self.rect)]

			return []

		def draw(self, surface):
			"""Rysuje pole na danej powierzchni oraz jeśli trzeba rysuje także reprezentacje modyfikatora."""

			surface.blit(self.image, self.rect.topleft)
			if self.getLogic().getItems():
				surface.blit(self.modifiers[MODIFIER_ITEM], self.rect.topleft)

			if self._showModifiers and self._logic.getModifier() and self.modifiers[self._logic.getModifier()]:
				surface.blit(self.modifiers[self._logic.getModifier()], self.rect.topleft)
