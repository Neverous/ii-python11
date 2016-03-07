# -*- encoding: utf8 -*-
import sys
import os
import pygame
from pygame.locals import *

def Cut(full, y, x, width, height, count):
	res = []
	for i in range(count):
		res.append(full.subsurface(((x, y), (width, height))))
		x += width

	return res

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Animacje')
clock = pygame.time.Clock()
full = pygame.image.load("sprite.png").convert()
drink = Cut(full, 581, 0, 40, 45, 17)
land = Cut(full, 427, 0, 39, 48, 13)
sneak = Cut(full, 753, 0, 38, 38, 8)
i = 0
while True:
	clock.tick(15)
	screen.blit(drink[i % len(drink)], (0, 50))
	screen.blit(land[i % len(land)], (50, 50))
	screen.blit(sneak[i % len(sneak)], (100, 50))

	pygame.display.update()
	i += 1
