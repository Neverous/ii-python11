# -*- encoding: utf8 -*-
import random
import codecs
import os
import time

#lista słów
words = codecs.open('slowa.txt', 'r', 'iso8859-2').read().split("\n")

MAX_TRIES = 5

HELP = """Witaj w grze w szubienicę! Wpisz:
	* quit, aby zakończyć,
	* literę, aby sprawdzić czy występuje w haśle,
	* przewidywane hasło, aby sprawdzić czy jest poprawne,
Masz %d prób. Każdy błąd(złe hasło, niewystępująca litera) to jedna próba.
""" % MAX_TRIES

GALLOWS = ("""






-------------
|           |
""","""
 
|
|
|
|
|
-------------
|           |
""", """
 __________
|          
|
|
|
|
-------------
|           |
""", """
 __________
|          |
|
|
|
|
-------------
|           |
""", """
 __________
|          |
|
|          O
|         /|\\
|         / \\
-------------
|           |
""", """
 __________
|          |
|          O
|         /|\\
|         / \\
|
-------------
|           |
""",
)

#STAN
tries = -1
word = ''
letters = [' ']

def clearScreen():
	"""Czyść ekran."""

	os.system('clear')

def startGame():
	"""Zacznij grę."""

	global tries, word, letters, words, HELP
	tries = 0
	word = random.choice(words).encode('utf8')
	letters = [' ']
	print HELP

def printWord():
	"""Wypisz aktualne hasło."""

	global word, letters

	print 'Hasło:', ''.join(map(lambda x: x in letters and x or '_', word))

def drawGallows():
	"""Rysuj szubienicę."""

	print GALLOWS[tries]

def doLetter(letter):
	"""Wpisano literę."""

	global letters, word, tries

	if letter in letters:
		print 'Litera już była sprawdzana!'
		return

	letters.append(letter)
	if not letter in word:
		tries += 1
		print 'Ta litera nie występuje w haśle. Pozostało %d prób!' % (MAX_TRIES - tries)
		return

	print 'Litera występuje w haśle!'

def doWord(guess):
	"""Wpisano hasło."""

	global word, tries

	if word != guess:
		tries += 1
		print 'Niepoprawne hasło! Pozostało %d prób!' % (MAX_TRIES - tries)

	else:
		tries = -1
		print 'To jest poprawne hasło! Gratulacje! Rozpoczynanie nowej gry.'

while True:
	clearScreen()
	if tries == -1:
		startGame()

	drawGallows()
	if tries >= MAX_TRIES:
		print 'Przekroczono liczbę prób! Poprawne hasło to:', word, 'Rozpoczynanie nowej gry.'
		tries = -1
		time.sleep(5)
		continue

	printWord()
	event = raw_input('>>').strip().lower()
	if event == 'quit':
		break

	if len(event) == 1: # Podano literkę
		doLetter(event)

	else: # Podano hasło
		doWord(event)

	time.sleep(2)

