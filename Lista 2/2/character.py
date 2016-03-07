# -*- encoding: utf8 -*-

class Character:
	def __init__(self, name):
		self.x = 320
		self.y = 240
		self.h = ''
		self.v = 'n'
		self.action = 'stop'
		self.name = name

	def getPosition(self):
		return (self.x, self.y)

	def getDirection(self):
		return (self.v + self.h) or 'n'

	def getAction(self):
		return self.action

	def getName(self):
		return self.name

