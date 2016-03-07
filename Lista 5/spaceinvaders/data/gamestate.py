# -*- encoding: utf8 -*-
import sys
import pygame
from pygame.locals import *
from utils import *
from spaceship import Spaceship
import level

class GameOver(Exception):
	pass

class GameWin(Exception):
	pass

class GameState:
	def __init__(self, screen):
		self.background = loadImage('data/gfx/background.jpg')
		screen.blit(self.background, (0, 0))
		self.x, self.y = screen.get_size()
		self.lives = 3
		self.level = 0
		self.score = 0
		self.dead = pygame.mixer.Sound('data/sound/dead.wav')
		self.nextLevel()

	def nextLevel(self):
		self.level += 1
		try:
			self.invaders, self.asteroids = level.load('data/level'+str(self.level)+'.dat', self)

		except:
			return False

		self.invaders = pygame.sprite.Group(self.invaders)
		self.asteroids = pygame.sprite.Group(self.asteroids)
		self.explosions = pygame.sprite.Group()
		self.bullets = pygame.sprite.Group()
		self.player = pygame.sprite.GroupSingle(Spaceship(self, 12 * 32 + 16, 18 * 32 + 16))
		return True

	def update(self):
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				raise KeyboardInterrupt()

			if event.type == KEYUP and event.key == K_TAB:
				pygame.display.toggle_fullscreen()

		if not self.player.sprite.health:
			self.dead.play()
			if not self.lives:
				raise GameOver()

			self.lives -= 1

		if not len(self.invaders) and not self.nextLevel():
			raise GameWin()

		if not self.player.sprite.health:
			self.player.add(Spaceship(self, 12 * 32 + 16, 18 * 32 + 16, cooldown = 80))

		toRemove = []
		for explosion in self.explosions:
			if explosion.health <= 0:
				toRemove.append(explosion)

		self.explosions.remove(toRemove)
		toRemove = []
		for bullet in self.bullets:
			if bullet.health <= 0:
				toRemove.append(bullet)

		self.bullets.remove(toRemove)
		toRemove = []
		for invader in self.invaders:
			if invader.health <= 0:
				toRemove.append(invader)

		self.invaders.remove(toRemove)
		toRemove = []
		for asteroid in self.asteroids:
			if asteroid.health <= 0:
				toRemove.append(asteroid)

		self.asteroids.remove(toRemove)
		self.explosions.update()
		self.bullets.update()
		self.invaders.update()
		self.asteroids.update()
		self.player.update()

	def draw(self, screen):
		screen.blit(self.background, (0, 0))
		self.asteroids.draw(screen)
		self.player.draw(screen)
		self.invaders.draw(screen)
		self.bullets.draw(screen)
		self.explosions.draw(screen)
