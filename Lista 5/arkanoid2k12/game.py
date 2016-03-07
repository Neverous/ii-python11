#!/usr/bin/python2
# -*- encoding: utf8 -*-
import sys
import pygame
sys.path.append('./data')
from engine import Engine

if __name__ == '__main__':
	pygame.init()
	pygame.mixer.init()
	pygame.display.set_caption('Arkanoid 2k12')
	engine = Engine()
	try:
		engine.run()

	except KeyboardInterrupt:
		pass
