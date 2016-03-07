# -*- encoding: utf-8 -*-
import random
import pygame
from utils import *

class Ball(pygame.sprite.Sprite):
	sound = None
	def __init__(self, scene, obj):
		super(Ball, self).__init__()
		self.obj = obj
		self.scene = scene
		self.image = pygame.Surface((16, 16))
		self.image.set_colorkey((0, 0, 0))
		pygame.draw.circle(self.image, (255, 255, 255), (8, 8), 8)
		self.rect = self.image.get_rect()
		self.rect.centerx, self.rect.centery = obj.rect.centerx, obj.rect.centery - 16
		self.gone = False
		self.inplace = True
		self.vx = 0
		self.vy = 0
		if not Ball.sound:
			Ball.sound = loadSound('data/snd/ballhit.wav')

		self.last = None

	def update(self):
		if self.inplace:
			self.rect.centerx, self.rect.centery = self.obj.rect.centerx, self.obj.rect.centery - 16
			return

		if abs(self.vx) < 1:
			self.shot()

		if abs(self.vy) < 1:
			self.shot()

		hit = []
		hit.extend(pygame.sprite.spritecollide(self, self.scene.balls, False, pygame.sprite.collide_rect))
		hit.extend(pygame.sprite.spritecollide(self, self.scene.bricks, False, pygame.sprite.collide_rect))
		hit.extend(pygame.sprite.spritecollide(self, self.scene.paddle, False, pygame.sprite.collide_rect))
		if hit:
			for box in hit:
				if box != self and self.last != box:
					self.last = box
					self.sound.play()
					box.hit(50)
					width, height = box.image.get_size()
					posx, posy = box.rect.centerx, box.rect.centery
					if self.rect.centerx <= box.rect.centerx and posy - height / 2 < self.rect.centery < posy + height / 2:
						self.vx *= -1 * (1 + random.randint(-5, 5) / 50.0)

					elif self.rect.centerx <= box.rect.centerx:
						self.vy *= -1 * (1 + random.randint(-5, 5) / 50.0)

					elif self.rect.centerx > box.rect.centerx and posy - height / 2 < self.rect.centery < posy + height / 2:
						self.vx *= -1 * (1 + random.randint(-5, 5) / 50.0)

					elif self.rect.centerx > box.rect.centerx:
						self.vy *= -1 * (1 + random.randint(-5, 5) / 50.0)

					break
		
		self.move()

	def shot(self):
		self.inplace = False
		self.vy = -random.choice((3, 4, 5, 6, 7))
		self.vx = random.choice((-7, -6, -5, -4, 4, 5, 6, 7))

	def hit(self, points):
		pass

	def move(self):
		resx, resy = self.scene.engine.getResolution()
		self.rect.centerx += self.vx
		self.rect.centery += self.vy
		if self.rect.centery - 8 > resy:
			self.gone = True

		if self.rect.centery - 8 <= 0:
			self.vy *= -1
			self.rect.centery = 9
			self.sound.play()
			self.last = None

		if self.rect.centerx - 8 <= 0:
			self.vx *= -1
			self.rect.centerx = 9
			self.sound.play()
			self.last = None

		if self.rect.centerx + 8 >= resx:
			self.vx *= -1
			self.rect.centerx = resx - 9
			self.sound.play()
			self.last = None
