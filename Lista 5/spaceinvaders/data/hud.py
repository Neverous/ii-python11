# -*- encoding: utf8 -*-
import pygame
import time
from pygame.locals import *
from utils import *

class HUD:
	def __init__(self, game):
		self.game = game
		self.x, self.y = 600, 0
		self.font = pygame.font.Font(pygame.font.get_default_font(), 14)
		self.lives = self.game.lives
		self.health = self.game.player.sprite.health
		self.level = self.game.level
		self.score = self.game.score
		self.loose = pygame.mixer.Sound('data/snd/loose.wav')
		self.win = pygame.mixer.Sound('data/snd/win.wav')
		self.nextlevel = pygame.mixer.Sound('data/snd/level.wav')

	def update(self):
		self.lives = self.game.lives
		self.health = self.game.player.sprite.health
		self.level = self.game.level
		self.score = self.game.score
	
	def draw(self, screen):
		text = self.font.render("Score: %d. Level: %d. Health: %d. Lives left: %d." % (self.score, self.level, self.health, self.lives), 1, (255, 255, 255))
		width, height = text.get_size()
		pygame.draw.rect(screen, (0, 0, 0), ((self.x - width / 2 - 5, self.y), (width + 10, height + 10))) 
		screen.blit(text, (self.x - width / 2, self.y + 5))

	def gameover(self, screen):
		screen.fill((0, 0, 0))
		text = self.font.render("Game Over! Score: %d." % (self.game.score), 1, (255,255,255))
		width, height = text.get_size()
		screen.blit(text, (self.game.x / 2 - width / 2, self.game.y / 2 - height / 2))
		pygame.display.update()
		self.loose.play()
		time.sleep(10)

	def gamewin(self, screen):
		screen.fill((0, 0, 0))
		text = self.font.render("Congratulations! Score: %d" % (self.game.score), 1, (255,255,255))
		width, height = text.get_size()
		screen.blit(text, (self.game.x / 2 - width / 2, self.game.y / 2 - height / 2))
		pygame.display.update()
		self.win.play()
		time.sleep(10)

	def nextLevel(self, screen):
		screen.fill((0, 0, 0))
		text = self.font.render("Level %d" % self.game.level, 1, (255,255,255))
		width, height = text.get_size()
		screen.blit(text, (self.game.x / 2 - width / 2, self.game.y / 2 - height / 2))
		pygame.display.update()
		self.nextlevel.play()
		time.sleep(3)
