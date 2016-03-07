#!/usr/bin/python2
# -*- encoding: utf8 -*-
# Maciej Szeptuch 2012

import sys
import pygame
import version
sys.path.append('./data')
import engine
from menu import Menu, ResolutionButton, FullscreenButton, ExitButton
from scene import NewGameButton
from editor import EditorButton
import utils

if __name__ == '__main__':
	pygame.init()
	pygame.mixer.init()
	pygame.display.set_caption(version.NAME + ' v' + version.VERSION)
	_engine = engine.Engine(len(sys.argv) > 1 and sys.argv[1] == '--debug') # --debug aby włączyć tryb testowy(pokazuje które części ekranu się odświeżają)
	pygame.display.set_icon(utils.loadImage('data/gfx/cursor/attack.png', alpha = True))
	_engine.addModule(Menu(_engine, (
		NewGameButton(_engine), # Nowa gra
		EditorButton(_engine), # Edytor
		ResolutionButton(_engine), # Rozdzielczosc
		FullscreenButton(_engine), # Pelny ekran/okno
		ExitButton(_engine), # Wyjscie
	)))
	_engine.activateModule('Menu')
	try:
		_engine.run()

	except KeyboardInterrupt:
		pass
