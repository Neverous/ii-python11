#!/usr/bin/python2
# -*- encoding: utf8 -*-
import sys
import pygame
sys.path.append('./data')
import gamestate
import hud

if __name__ == '__main__':
	pygame.init()
	pygame.mixer.pre_init(44100, -16, 2)
	pygame.mixer.init()
	screen = pygame.display.set_mode((800, 640))
	pygame.display.set_caption("Space Invaders")
	pygame.mouse.set_visible(False)
	clock = pygame.time.Clock()
	game = gamestate.GameState(screen)
	hud = hud.HUD(game)
	last = game.level
	try:
		while True:
			clock.tick(30)
			game.update()
			hud.update()
			game.draw(screen)
			hud.draw(screen)
			pygame.display.update()
			if game.level != last:
				last = game.level
				hud.nextLevel(screen)

	except KeyboardInterrupt:
		pass

	except gamestate.GameOver:
		hud.gameover(screen)

	except gamestate.GameWin:
		hud.gamewin(screen)
