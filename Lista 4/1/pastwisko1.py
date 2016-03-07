#!/usr/bin/env python

import pygame
from pygame.locals import *
from sys import exit
from krowa2 import Cow

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Pastwisko")


cow_images = []
nazwy = [ "cowImages/walking e" + str(i) + ".png" for i in range(1,8)]
for n in nazwy:
	cow_images.append(pygame.image.load(n).convert_alpha())

clock = pygame.time.Clock()

circle = [(0, 0), 0]
cows = []
for i in range(7):
	for j in range(5):
		cows.append( Cow((100*i,100*j), cow_images, circle))

stado = pygame.sprite.Group(cows)
drawCircle = False

while True:
	clock.tick(30)
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()

		if event.type == MOUSEBUTTONDOWN:
			drawCircle = True
			startpos = endpos = event.pos
			circle[0] = ((startpos[0] + endpos[0]) / 2, (startpos[1] + endpos[1]) / 2)
			circle[1] = max(abs(startpos[0] - endpos[0]) / 2, abs(startpos[1] - endpos[1]) / 2)

		if event.type == MOUSEBUTTONUP:
			drawCircle = False

		if drawCircle and event.type == MOUSEMOTION:
			endpos = event.pos
			circle[0] = ((startpos[0] + endpos[0]) / 2, (startpos[1] + endpos[1]) / 2)
			circle[1] = max(abs(startpos[0] - endpos[0]) / 2, abs(startpos[1] - endpos[1]) / 2)

	screen.fill( (70,200,10) )
	pygame.draw.circle(screen, (30,70,0), circle[0], circle[1])
	stado.update()
	stado.draw(screen)
	pygame.display.update()
