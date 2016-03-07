#!/usr/bin/python2
# -*- encoding: utf8 -*-
import sys
import pygame
sys.path.append('./data')
from engine import Engine

if __name__ == '__main__':
	pygame.init()
	pygame.mixer.init()
	pygame.display.set_caption('Tanks 2k12')
	debug = len(sys.argv) > 1 and sys.argv[1] == '--debug'
	engine = Engine(debug)
	try:
		engine.run()

	except KeyboardInterrupt:
		pass
