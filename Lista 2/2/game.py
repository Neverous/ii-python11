# -*- encoding: utf8 -*-
import sys
import os
import pprint
import pygame
import math
from pygame.locals import *
from character import Character
from collections import defaultdict

pygame.init()
screen = pygame.display.set_mode((640, 480))

# Load images
def factory():
	return defaultdict(factory)

images = factory()
for path, _, files in os.walk('img'):
	if not files:
		continue

	act = images
	for name in path.split('/')[1:]:
		act = act[name]

	for filename in files:
		name = os.path.splitext(filename)[0]
		try:
			act[name] = pygame.image.load(os.path.join(path, filename)).convert()
			if name != 'grass':
				act[name].set_colorkey(act[name].get_at((0, 0)))

		except:
			print 'WARNING:', path, filename

background = pygame.Surface(screen.get_size())
i = 0
while i < 640:
	j = 0
	while j < 640:
		background.blit(images['grass'], (i, j))
		j += images['grass'].get_size()[1]

	i += images['grass'].get_size()[0]



character = (Character('croc'), Character('harry'))
before = False
c = 0
a = 0
i = 0
aspeed = 15
while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			sys.exit(0)

	pressed = pygame.key.get_pressed()
	if True in (pressed[K_UP], pressed[K_LEFT], pressed[K_DOWN], pressed[K_RIGHT]):
		character[c].action = 'walk'
		delta = 1
		aspeed = 15
		if pressed[K_LSHIFT] | pressed[K_RSHIFT]:
			character[c].action = 'run'
			delta = 2

		y = 0
		x = 0
		if pressed[K_UP]:
			character[c].v = 'n'
			character[c].y -= delta
			y = 1

		elif pressed[K_DOWN]:
			character[c].v = 's'
			character[c].y += delta
			y = -1

		else:
			character[c].v = ''

		if pressed[K_LEFT]:
			character[c].h = 'w'
			character[c].x -= delta
			x = 1

		elif pressed[K_RIGHT]:
			character[c].h = 'e'
			character[c].x += delta
			x = -1

		else:
			character[c].h = ''

		if pressed[K_LEFT] and pressed[K_RIGHT]:
			character[c].h = 'e'

		if pressed[K_UP] and pressed[K_DOWN]:
			character[c].v = 's'

		if x and y:
			character[c].x += x * (delta - math.sqrt(0.5 * delta ** 2))
			character[c].y += y * (delta - math.sqrt(0.5 * delta ** 2))

	else:
		if pressed[K_RCTRL] | pressed[K_LCTRL]:
			character[c].action = 'attack'
			aspeed = 15
			before = False

		elif pressed[K_RALT] | pressed[K_LALT]:
			character[c].action = 'look'
			aspeed = 15
			before = False

		elif pressed[K_q]:
			if not before:
				c = not c

			before = True

		elif pressed[K_SPACE]:
			character[c].action = 'talk'
			aspeed = 15
			before = False

		elif pressed[K_z]:
			character[c].action = 'tip'
			aspeed = 15
			before = False

		elif pressed[K_x]:
			character[c].action = 'hit'
			aspeed = 15
			before = False

		else:
			character[c].action = 'stop'
			aspeed = 15
			before = False

	img = images[character[c].getName()][character[c].getAction()][character[c].getDirection()+str(a)]
	if not isinstance(img, pygame.Surface):
		a = 0
		img = images[character[c].getName()][character[c].getAction()][character[c].getDirection()+str(a)]

	if character[c].getPosition()[0] > screen.get_size()[0]:
		character[c].x = screen.get_size()[0]

	elif character[c].getPosition()[0] < 0:
		character[c].x = 0

	if character[c].getPosition()[1] > screen.get_size()[1]:
		character[c].y = screen.get_size()[1]

	elif character[c].getPosition()[1] < 0:
		character[c].y = 0

	screen.blit(background, (0, 0))
	pos = character[c].getPosition()
	pos = (pos[0] - img.get_size()[0] / 2, pos[1] - img.get_size()[1] / 2)
	screen.blit(img, pos)
	pygame.display.update()
	if i % aspeed == 0:
		i = 0
		a += 1

	i += 1
