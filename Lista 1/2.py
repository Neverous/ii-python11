# -*- encoding: utf8 -*-
import sys
import time
import random
import pygame
from pygame.locals import *

MAX_CIRCLE = 200

def drawLinearGradient(surface, start, end, startColor, endColor):
	"""Rysuje gradient od lewej do prawej w polu wyznaczonym przez punkty start
	i end, zaczynając od koloru startColor przechodząc do endColor."""

	step = (
		1.0 * (endColor[0] - startColor[0]) / (end[0] - start[0] - 1),
		1.0 * (endColor[1] - startColor[1]) / (end[0] - start[0] - 1),
		1.0 * (endColor[2] - startColor[2]) / (end[0] - start[0] - 1),
	)

	color = startColor
	for w in range(start[0], end[0]):
		pygame.draw.line(surface, color, (w, start[1]), (w, end[1]))
		color = [color[c] + step[c] for c in range(3)]

	return

def drawCircleGradient(surface, center, radius, startColor, endColor):
	"""Rysuje gradient kołowy o środku w punkcie center i promieniu radius,
	zaczynając od koloru startColor przechodząc do endColor."""

	step = (
		1.0 * (endColor[0] - startColor[0]) / (radius - 1),
		1.0 * (endColor[1] - startColor[1]) / (radius - 1), 
		1.0 * (endColor[2] - startColor[2]) / (radius - 1),
	)

	color = list(startColor)
	for r in range(radius + 1, 1, -1):
		pygame.draw.circle(surface, color, center, r)
		color = [color[c] + step[c] for c in range(3)]

	return

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.mouse.set_visible(False)
background = pygame.Surface(screen.get_size())

# TŁO
drawLinearGradient(background, (0, 0), (320, 240), (200, 80, 75), (56, 253, 0))
drawLinearGradient(background, (320, 0), (640, 240), (20, 80, 123), (56, 43, 0))
drawLinearGradient(background, (0, 240), (320, 480), (70, 47, 5), (79, 253, 0))
drawLinearGradient(background, (320, 240), (640, 480), (40, 8, 75), (56, 83, 151))

drawCircleGradient(background, (320, 240), 100, (255, 255, 255), (0, 0, 0))

screen.blit(background, (0, 0))
pygame.display.update()

pkt = (0, 0)
while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			sys.exit(0)
		
		if event.type == MOUSEMOTION:
			pkt = event.pos
			
	if pkt[0] > 0:
		screen.blit(background, (0, 0))
		pygame.draw.circle(screen, screen.get_at(pkt), pkt, pkt[0] * MAX_CIRCLE / 640)
		pygame.draw.circle(screen, (0, 0, 0), pkt, max(pkt[0] * MAX_CIRCLE / 640, 1), 1)
		pygame.display.update()   
