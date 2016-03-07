# -*- encoding: utf8 -*-
import sys
import os
import pygame
from pygame.locals import *

LINE = 4
CIRCLE = 6

def inCircle(point, center, radius):
	return (center[0] - point[0]) ** 2 + (center[1] - point[1]) ** 2 <= radius ** 2

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Edytor Jednej Kreski')
if len(sys.argv) < 2:
	print "Podaj obrazek tła!"
	sys.exit(0)

background = pygame.image.load(sys.argv[1]).convert()
circles = []
try:
	for circle in open(sys.argv[1] + '.pts', 'r').read().split("\n"):
		circle = tuple(map(int, circle.split()))
		if len(circle) != 2:
			continue

		circles.append(circle)

except:
	circles = []

movingCircle = -1
try:
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				raise KeyboardInterrupt()

			if event.type == MOUSEBUTTONDOWN:
				new = True
				for i, circle in enumerate(circles):
					if inCircle(event.pos, circle, CIRCLE):
						new = False
						if event.button == 3:
							del circles[i]

						else:
							movingCircle = i

						break

				if event.button == 1 and new:
					circles.append(event.pos)

			if event.type == MOUSEBUTTONUP:
				movingCircle = -1

			if movingCircle != -1 and event.type == MOUSEMOTION:
				circles[movingCircle] = event.pos

		screen.blit(background, (0,0))
		if len(circles) > 1:
			pygame.draw.lines(screen, (255, 0, 0), False, circles, LINE)

		for i, circle in enumerate(circles):
			color = (255, 0, 0)
			if i == movingCircle:
				color = (0, 255, 0)

			pygame.draw.circle(screen, color, circle, CIRCLE)

		pygame.display.update()

except KeyboardInterrupt:
	pass

file = open(sys.argv[1] + '.pts', 'w')
for circle in circles:
	print >>file, ' '.join(map(str, circle))

file.close()
