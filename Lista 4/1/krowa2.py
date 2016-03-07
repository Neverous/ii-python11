#!/usr/bin/env python

import pygame
import random
import math

def in_circle(point, circle):
    return (circle[0][0] - point[0]) ** 2 + (circle[0][1] - point[1]) ** 2 <= circle[1] ** 2

   
   
class Cow(pygame.sprite.Sprite):
  def __init__(self,  pos, images, circle):
     pygame.sprite.Sprite.__init__(self)
     self.x, self.y = pos
     self.vx = self.vy = 0
     self.images = images
     self.image = images[0]
     self.rect = self.image.get_rect()
     self.rect.centerx = self.x
     self.rect.centery = self.y
     self.patiency = random.randint(60,100)
     self.cow_nr = 0
     self.circle = circle

     
  def update(self):
     if self.patiency > 0:

        if in_circle((self.x, self.y), self.circle):
           self.x += self.vx / 10
           self.y += self.vy / 10
        else:
           self.x += self.vx
           self.y += self.vy

        if self.x < 0: 
          self.x = 0
          self.vx = -self.vx
        if self.y < 0: 
          self.y = 0
          self.vy = -self.vy
        if self.x > 640: 
          self.x = 640
          self.vx = -self.vx
        if self.y > 480: 
          self.y = 480
          self.vy = -self.vy
        self.patiency -= 1
     elif self.patiency <= 0:
        self.patiency = random.randint(60,100)
        self.vx,self.vy = rand_v()
        if self.circle[1] and not in_circle((self.x, self.y), self.circle) and random.randint(1, 3) == 2:
          if self.x < self.circle[0][0]:
            self.vx = abs(self.vx)

          if self.x > self.circle[0][0]:
            self.vx = -abs(self.vx)

          if self.x == self.circle[0][0]:
            self.vx = 0

          if self.y < self.circle[0][1]:
            self.vy = abs(self.vy)

          if self.y > self.circle[0][1]:
            self.vy = -abs(self.vy)

          if self.y == self.circle[0][1]:
            self.vy = 0
     
     self.rect.centerx = int(self.x)
     self.rect.centery = int(self.y)
        
     self.cow_nr = (self.cow_nr + 1) % 7
     self.image = self.images[self.cow_nr]
     
        
def rand_v():
   dx = random.randint(-1000,1000)
   dy = random.randint(-1000,1000)
   speed = random.randint(1,100) / 30.0
   
   if random.randint(0,30) == 0:
     speed += 4
     speed *= 3
   rand_len = math.sqrt(dx*dx +dy*dy)
   if rand_len == 0:
      return (0,0)
   dx = dx / rand_len * speed
   dy = dy / rand_len *speed
   return dx,dy
   

