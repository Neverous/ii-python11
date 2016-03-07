# -*- encoding: utf8 -*-
import sys
import pygame
from pygame.locals import *
from utils import *
from asteroid import Asteroid
from invader import Invader
def load(filename, game):
	invaders = []
	asteroids = []
	data = open(filename).read()
	r = 0
	for line in data.split("\n"):
		c = 0
		for letter in line:
			if letter == '7':
				asteroids.append(Asteroid(game, c * 32 + 16, r * 32 + 16))

			elif letter != '0':
				invaders.append(Invader(game, c * 32 + 16, r * 32 + 16, letter))

			c += 1

		r += 1

	return (invaders, asteroids)
