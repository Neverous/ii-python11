# -*- encoding: utf-8 -*-
import random
import pygame
from ball import Ball
from utils import *

class Bonus(pygame.sprite.Sprite):
	sound = None
	def __init__(self, scene, pos):
		super(Bonus, self).__init__()
		self.scene = scene
		self.image = pygame.Surface((18, 18))
		self.image.set_colorkey((0, 0, 0))
		self.type = random.randint(0, 2)
		self.image.fill([255 * (self.type + 1) / 3 for i in range(3)])
		self.rect = self.image.get_rect()
		self.rect.centerx, self.rect.centery = pos
		self.gone = False
		self.vy = random.randint(5, 16)
		if not Bonus.sound:
			Bonus.sound = loadSound('data/snd/bonushit.wav')

	def update(self):
		hit = []
		hit.extend(pygame.sprite.spritecollide(self, self.scene.paddle, False, pygame.sprite.collide_rect))
		resx, resy = self.scene.engine.getResolution()
		if hit or self.rect.centery - 9 > resy:
			self.gone = True

		if hit:
			self.sound.play()
			if self.type == 1:
				new = []
				balls = random.randint(1, 4)
				for b in self.scene.balls:
					for _ in range(balls):
						ball = Ball(self.scene, b)
						ball.rect.centery += 16
						ball.vx = b.vx + random.randint(-7, 7)
						ball.vy = b.vy + random.randint(-7, 7)
						ball.inplace = False
						ball.move()
						new.append(ball)

				for ball in new:
					self.scene.balls.add(ball)

			if self.type == 2:
				width, height = self.scene.paddle.sprite.image.get_size()
				temp = self.scene.paddle.sprite.rect.centerx, self.scene.paddle.sprite.rect.centery
				self.scene.paddle.sprite.image = pygame.transform.scale(self.scene.paddle.sprite.image, (width / 2, height))
				self.scene.paddle.sprite.rect = self.scene.paddle.sprite.image.get_rect()
				self.scene.paddle.sprite.rect.centerx, self.scene.paddle.sprite.rect.centery = temp

			if self.type == 0:
				self.scene.engine.player['lives'] += 1

		self.move()

	def move(self):
		self.rect.centery += self.vy
