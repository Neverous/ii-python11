import random
import pygame
pygame.init()
# MOUNTAINS
mountains = pygame.Surface((640, 480))
mountains.set_colorkey((0,)*3)
def drawMountains(surface, color, height, space):
	points = [(0, 480)]
	pos = 0
	while pos < 640:
		points.append((pos, random.randint(*reversed(map(lambda x: 480 - x, height)))))
		pos += random.randint(1, space)

	points.append((640, points[1][1]))
	points.append((640, 480))
	pygame.draw.polygon(surface, color, points)

drawMountains(mountains, (16,)*3, (300, 440), 128)
drawMountains(mountains, (32,)*3, (200, 320), 64)
drawMountains(mountains, (64,)*3, (140, 300), 32)
drawMountains(mountains, (128,)*3, (40, 200), 16)

background = pygame.Surface((640, 480))
background.fill((27, 204, 224))
background.blit(mountains, (0, 0))
pygame.image.save(background, 'mountains.jpg')

# CITY

city = pygame.Surface((640, 480))
city.set_colorkey((50,)*3)
city.fill((50,)*3)
pos = 5
while pos < 640:
	width = 30
	if width + pos > 640:
		break

	height = random.randint(150, 300)
	pygame.draw.rect(city, (0,)*3, (pos, 480 - height, width, height))
	pos += width + 10

background = pygame.Surface((640, 480))
background.fill((27, 204, 224))
background.blit(city, (0, 0))
pygame.image.save(background, 'city.jpg')


# FOREST
forest = pygame.Surface((640, 480))
forest.set_colorkey((50,)*3)
forest.fill((50,)*3)
def drawTree(surface, center, width):
	height = random.randint(width * 4, 80)
	pygame.draw.rect(surface, (50, 20, 0), (center - width / 2, 480 - height, width, height))
	pygame.draw.circle(surface, (50, 125, 0), (center, 480 - height), width * 2)

pos = 20
while pos <= 620:
	drawTree(forest, pos, 10)
	pos += random.randint(15, 60)

pos = 620
while pos >= 20:
	drawTree(forest, pos, 10)
	pos -= random.randint(15, 60)

background = pygame.Surface((640, 480))
background.fill((27, 204, 224))
background.blit(forest, (0, 0))
pygame.image.save(background, 'forest.jpg')

# COMBO ;p
background = pygame.Surface((640, 480))
background.fill((27, 204, 224))
background.blit(mountains, (0, 0))
#background.blit(city, (0, 0))
background.blit(forest, (0, 0))
pygame.image.save(background, 'combo.jpg')
