# -*- encoding: utf-8 -*-
import pygame
import time
import random
from pygame.locals import *
from utils import *
import engine
from brick import Brick
from paddle import Paddle
from ball import Ball

class SceneOut(Exception): pass
class NextLevel(Exception): pass
class GameWin(Exception): pass
class GameOver(Exception): pass

def makeBricks(scene, res, definition):
	bricks = []
	width = res[0] / 20
	height = width / 2
	x = width
	y = height
	r = 0
	for row in definition:
		c = 0
		for type in row:
			bricks.append(Brick(scene, type, (x + c * width, y + r * height), (width * 8 / 10, height * 8 / 10)))
			c += 1

		r += 1

	return bricks

class Scene(object):
	sounds = None
	images = None
	def __init__(self, engine, level):
		self.engine = engine
		if not Scene.sounds:
			Scene.sounds = (
				loadSound('data/snd/gameloop1.wav'),
				loadSound('data/snd/gameloop2.wav'),
				loadSound('data/snd/gameloop3.wav'),
				loadSound('data/snd/gameloop4.wav'),
				loadSound('data/snd/gameloop5.wav'),
				loadSound('data/snd/gameloop6.wav'),
			)

		if not Scene.images:
			Scene.images = loadImages('data/gfx/').values()

		width, height = self.engine.getResolution()
		self.image = random.choice(self.images)
		self.background = pygame.transform.smoothscale(self.image, (width, height))
		self.surface = self.background.copy()
		self.last = random.choice(self.sounds)
		self.lastEnd = 0
		self.bricks = pygame.sprite.Group(makeBricks(self, (width, height), level))
		self.paddle = pygame.sprite.GroupSingle((Paddle(self, (width / 2, height - 50)),))
		self.balls = pygame.sprite.Group((Ball(self, self.paddle.sprite), ))
		self.anibricks = pygame.sprite.Group()
		self.bonus = pygame.sprite.Group()

	def show(self):
		self.last.play(-1)
		self.lastEnd = time.time() + random.randint(60, 120)
		while True:
			try:
				self.playMusic()
				self.engine.tick()
				for event in pygame.event.get():
					if event.type == QUIT:
						raise KeyboardInterrupt()

					if event.type == KEYUP and event.key == K_ESCAPE:
						raise SceneOut()


					if self.engine.getControls() & engine.CONTROLS_MOUSE:
						if event.type == MOUSEMOTION:
							self.paddle.sprite.move(event.pos[0])

						if event.type == MOUSEBUTTONUP and event.button == 1:
							for ball in self.balls:
								if ball.inplace:
									ball.shot()

					if self.engine.getControls() & engine.CONTROLS_KEYBOARD:
						if event.type == KEYUP and event.key == K_SPACE:
							for ball in self.balls:
								if ball.inplace:
									ball.shot()

				if self.engine.getControls() & engine.CONTROLS_KEYBOARD:
					if pygame.key.get_pressed()[K_LEFT]:
						self.paddle.sprite.move(self.paddle.sprite.rect.centerx - 10)

					elif pygame.key.get_pressed()[K_RIGHT]:
						self.paddle.sprite.move(self.paddle.sprite.rect.centerx + 10)


				if self.engine.state & engine.STATE_WIN or self.engine.state & engine.STATE_FAIL:
					continue

				toRemove = []
				for bonus in self.bonus:
					if bonus.gone:
						toRemove.append(bonus)

				self.bonus.remove(toRemove)
				toRemove = []
				for brick in self.anibricks:
					if brick.gone:
						toRemove.append(brick)

				self.anibricks.remove(toRemove)

				toRemove = []
				for brick in self.bricks:
					if brick.gone:
						toRemove.append(brick)

				self.bricks.remove(toRemove)
				toRemove = []
				for ball in self.balls:
					if ball.gone:
						toRemove.append(ball)

				self.balls.remove(toRemove)

				self.bonus.update()
				self.paddle.update()
				self.balls.update()
				self.bricks.update()
				self.anibricks.update()

				if not len(self.bricks):
					if not self.engine.nextLevel():
						raise GameWin()

					else:
						raise NextLevel()

				if not len(self.balls):
					self.engine.player['lives'] -= 1
					if not self.engine.player['lives']:
						raise GameOver()

					width, height = self.engine.getResolution()
					self.paddle.add(Paddle(self, (width / 2, height - 50)))
					self.balls = pygame.sprite.Group([Ball(self, self.paddle.sprite)])

				# Draw all to screen
				self.surface.blit(self.background, (0, 0))
				self.bricks.draw(self.surface)
				self.paddle.draw(self.surface)
				self.balls.draw(self.surface)
				self.anibricks.draw(self.surface)
				self.bonus.draw(self.surface)
				# write HUD
				resx, resy = self.engine.getResolution()
				self.engine.writeText(self.surface, "Punkty: %d Zycia: %d" % (self.engine.player['score'], self.engine.player['lives']), 14, (255, 255, 255), (resx / 2, resy - 15))
				self.engine.screen.blit(self.surface, (0, 0))
				pygame.display.update()

			except SceneOut:
				self.engine.state ^= engine.STATE_GAME | engine.STATE_MENU
				break

			except NextLevel:
				self.surface.blit(self.background, (0, 0))
				resx, _ = self.engine.getResolution()
				self.engine.writeText(self.surface, "Nastepny poziom!", 36, (255, 255, 255), (resx / 2, 100))
				self.engine.screen.blit(self.surface, (0, 0))
				pygame.display.update()
				time.sleep(3)
				break

			except GameOver:
				self.surface.blit(self.background, (0, 0))
				resx, _ = self.engine.getResolution()
				self.engine.writeText(self.surface, "Game Over!", 48, (255, 255, 255), (resx / 2, 100))
				self.engine.state |= engine.STATE_FAIL
				self.engine.screen.blit(self.surface, (0, 0))
				pygame.display.update()

			except GameWin:
				self.surface.blit(self.background, (0, 0))
				resx, _ = self.engine.getResolution()
				self.engine.writeText(self.surface, "Gratulacje!", 48, (255, 255, 255), (resx / 2, 100))
				self.engine.state |= engine.STATE_WIN
				self.engine.screen.blit(self.surface, (0, 0))
				pygame.display.update()

		self.last.fadeout(1500)

	def playMusic(self, anyway = False):
		if not anyway and self.lastEnd > time.time():
			return

		self.lastEnd = time.time() + random.randint(60, 120)
		self.last.fadeout(1500)
		self.last = random.choice(self.sounds)
		self.last.play(-1)

	def screenUpdated(self):
		self.background = pygame.transform.smoothscale(self.image, self.engine.getResolution())
		self.surface = pygame.transform.smoothscale(self.surface, self.engine.getResolution())
