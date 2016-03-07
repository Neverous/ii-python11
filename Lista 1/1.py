# -*- encoding: utf-8 -*-
import math
import pygame
from pygame.locals import *
from sys import exit

def dist(a, b):
   """Odległość między punkatmi a i b"""
   return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def inInterval(point, start, end):
   """Czy punkt znajduje się w prostokącie wyznaczanym przez start i end"""
   return min(start[0], end[0]) <= point[0] <= max(start[0], end[0]) and \
          min(start[1], end[1]) <= point[1] <= max(start[1], end[1])

def pointInDistance(a, b, length):
   """Zwraca punkt na lini a-b w odległości(w przybliżeniu) length od b."""

   x1, y1 = a
   x2, y2 = b
   if x2 == x1:
      return (x2, y2 - length)

   if y2 == y1:
      return (x2 - length, y2)

   c = 1.0 * (y2 - y1) / (x2 - x1)
   X1 = 1.0 * (x2*(c*c + 1) - math.sqrt((c*c + 1)*length**2)) / (c*c + 1)
   Y1 = c * (X1 - x2) + y2
   X2 = 1.0 * (x2*(c*c + 1) + math.sqrt((c*c + 1)*length**2)) / (c*c + 1)
   Y2 = c * (X2 - x2) + y2
   if inInterval((X1, Y1), a, b):
      return (X1, Y1)

   else:
      return (X2, Y2)

class Line(list):
   """Linia o stałej(w przybliżeniu) długości."""
   def __init__(self, length, maxsize = 1024):
      super(Line, self).__init__()
      self.maxsize = maxsize
      self.length = length
      self.actual = 0

   def append(self, point):
      super(Line, self).append(point)
      if len(self) == self.maxsize:
         self.actual -= dist(self[0], self[1])
         del self[0]

      if len(self) <= 1:
         return

      self.actual += dist(self[-1], self[-2])
      while self.actual > self.length + 1:
         part = dist(self[0], self[1])
         # jeśli można wyrzucić ostatni punkt i nadal będzie za dużo bądź równo
         if self.actual - part >= self.length:
            self.actual -= part
            del self[0]

         # w przeciwnym przypadku przesuń ostatni punkt
         # PRZYBLIŻENIE
         else:
            self[0] = pointInDistance(self[0], self[1], part - self.actual + self.length)
            self.actual -= part - dist(self[0], self[1])
      
pygame.init()
ekran = pygame.display.set_mode((640,480))
linia = Line(100)
linia.append((0, 0))

while True:
   for zdarzenie in pygame.event.get():
      if zdarzenie.type == QUIT:
         exit(0)

      if zdarzenie.type == MOUSEMOTION:
         linia.append(zdarzenie.pos)

   ekran.fill((255,255,255))
   if len(linia) > 1:
      pygame.draw.lines(ekran, (70,255,10), False, linia, 2)

   pygame.display.update()   
