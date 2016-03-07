#!/usr/bin/env python

import pygame
from pygame.locals import *
from sys import exit
from random import randint

rysunek = []
for i in range(48):
	rysunek.append( 64 * [(255, 255, 255)])

def uaktualnijRysunek(pos,color):
	xm,ym = event.pos
	x = xm/10
	y = ym/10
	if x >=0 and x<64 and y >= 0 and y < 48:
		rysunek[y][x] = color

pygame.init()
screen = pygame.display.set_mode((640, 480))

points = []
myszkaSieRusza = False
while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()

		if event.type == MOUSEBUTTONDOWN:
			myszkaSieRusza = True
			if event.button == 1:
				color = (0, 0, 0)

			else:
				color = (255, 255, 255)

			uaktualnijRysunek(event.pos,color)

		if event.type == MOUSEMOTION:
			if myszkaSieRusza:
				uaktualnijRysunek(event.pos,color)

		if event.type == MOUSEBUTTONUP:
			myszkaSieRusza = False


	screen.fill((255,255,255))

	for i in range(48):
		for j in range(64):
			pygame.draw.rect(screen,rysunek[i][j], pygame.Rect(10*j,10*i,10,10) )

	pygame.display.update()

