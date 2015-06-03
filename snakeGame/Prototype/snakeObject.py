#!/usr/bin/env python3
#Python Studies; Manoel Vilela; 29/01/2015
#
#Snake Game Clone with Pygame
#
#Testing concepts of OO
#Contact: manoel_vilela@engineer.com

from pygame.locals import *
import pygame, time
from time import localtime
from random import randint


WIDTH, HEIGHT = 400, 400; SIZESCREEN = WIDTH, HEIGHT; FPS = 10; MODE = 0; HIGHSCORE = 0; COLISIONDEATH = False
SIZECELL = 20
CELLWIDTH = WIDTH // SIZECELL
CELLHEIGHT = HEIGHT // SIZECELL
BLUE = (0, 0, 255); RED = (255, 0, 0); BLACK = (0, 0, 0); WHITE = (255, 255, 255)

class cell(object):
	def __init__ (self, x, y, a, b, color = BLUE):
		self.x = x
		self.y = y
		self.color = color
		self.width = a
		self.height = b
		self.rect = pygame.Rect(x, y, a, b)
	def move(self, position):
		self.x, self.y = position
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
	def draw(self, screen):
		color = self.color
		pygame.draw.rect(screen, color, self.rect)

class snake(cell):
	def __init__(self,
				 x = randint(0, WIDTH),
				 y = randint(0, HEIGHT),
				 a = CELLWIDTH, 
				 b = CELLHEIGHT):
		head = cell(x, y, a, b) 
		tail = cell(x, (y + a), a, b)
		self.cells = [head, tail]
		global keys, motion
		self.move = motion['UP']
	def controlUpdate(self):
		for key in keys.keys():
			if keys[key] == True:
				for a, b in [('UP', 'DOWN'), ('DOWN', 'UP'), ('LEFT', 'RIGHT'), ('RIGHT', 'LEFT')]:
					if self.move == motion[a] and key == b:
						return None
				self.move = motion[key] 	#UP, LEFT, DOWN RIGHT
				break
	def moveSnake(self):
		dx, dy = self.move
		head = self.cells[0]
		beforeCell = head.x, head.y
		x, y = beforeCell
		x += dx
		y += dy
		
		self.cells[0].move((x, y))
		
		for c in self.cells[1:]:
			lastCoord = c.x, c.y
			c.move(beforeCell)
			beforeCell = lastCoord			
			
	def colisionScreen(self, colisionDeath = True, xsize = WIDTH, ysize = HEIGHT):
		x_lim, y_lim = xsize - CELLWIDTH, ysize - CELLHEIGHT
		head = self.cells[0]
		x, y = head.x, head.y
		if x > x_lim or x < 0:
			if not colisionDeath:
				if x > x_lim:
					self.cells[0].move((0, y))
				else:
					self.cells[0].move((x_lim, y))
			else:
				return True
		if y > y_lim or y < 0:
			if not colisionDeath:
				if y > y_lim:
					self.cells[0].move((x, 0))
				else:
					self.cells[0].move((x, y_lim))
			else:
				return True
		return False
	def foodColision(self, food):
		head = self.cells[0]
		headRect = head.rect
		x, y = food.center
		if isPointInsideRect(x, y, headRect):
			a, b = food.size
			x, y = food.x, food.y
			newCell = cell(x, y, a, b)
			self.cells.insert(0, newCell)
			return True
		return False
	def selfColision(self): 
		head = self.cells[0].rect
		x, y = head.center
		for c in self.cells[1:]:
			c = c.rect
			if isPointInsideRect(x, y, c):
				return True
		return False
		
	def draw(self, screen):
		for c in self.cells:
			c.draw(screen)

def isPointInsideRect(x, y, rect):
	if (x > rect.left) and (x < rect.right) and (y > rect.top) and (y < rect.bottom):
		return True
	else:
		return False

def pause(screen, mensagem1, mensagem2 = ''):
	while True:
		screen.fill(BLACK)


		title = pygame.font.Font('freesansbold.ttf', 25)
		titleSurf = title.render("SnakeGame", True, WHITE)
		titleRect = titleSurf.get_rect()
		titleRect.midright = (int(WIDTH * 3/4 - 20), 10)
		screen.blit(titleSurf, titleRect)

		message = pygame.font.Font('freesansbold.ttf', 40)
		messageSurf = message.render(mensagem1, True, WHITE)
		messageRect = messageSurf.get_rect()
		messageRect.midleft = (int(WIDTH* 1/4), HEIGHT//2)
		screen.blit(messageSurf, messageRect)

		message = pygame.font.Font('freesansbold.ttf', 40)
		messageSurf = message.render(mensagem2, True, WHITE)
		messageRect = messageSurf.get_rect()
		messageRect.midleft = (int(WIDTH* 1/4), int( HEIGHT * 3/4))
		screen.blit(messageSurf, messageRect)
		
		pygame.display.update()
		mainClock = pygame.time.Clock()
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				quit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					return False
				if event.key == K_RETURN:
					return True
			mainClock.tick(FPS)

def writeHighscore():
	with open('highscore.txt', '+r') as rankdb:
		t = localtime()
		day, month, year = t.tm_mday, t.tm_mon, t.tm_year
		hour, minute, second = t.tm_hour, t.tm_min, t.tm_sec
		time = " | %s:%s:%s %s/%s/%s" %(hour, minute, second, day, month, year)

		data = rankdb.read()
		beforeData = data
		data = data.split('\n')
		scores = []
		
		for line in data:
			for score in line.split('|'):
				score = score.strip()
				if score.isdecimal():
					score = int(score)
					scores.append(score)

		print("HIGHSCORES:")
		print(beforeData, end = '')
		write = True
		if len(scores) > 0:
			if HIGHSCORE > max(scores):
				write = True
			else:
				write = False
		if write:
			string = "%4d %s\n" %(HIGHSCORE, time)
			w = rankdb.write(string)
			print(string)
			print("Novo HIGHSCORE! %d" %HIGHSCORE)

def playerControl(snake, screen):
	snake.controlUpdate()
	snake.moveSnake()
	snake.draw(screen)

def foodControl(screen, player, food, score):
	if food != None:
		food.draw(screen)
		if player.foodColision(food.rect) == True:
			food = None
			print("ColisionFood")
		elif player.selfColision() or player.colisionScreen(COLISIONDEATH):
			print("SelfColision or ColisionScreen")
			question = pause(screen, 'GameOver', 'Score: %d' %score)
			if question:
				return game()
			else:
				return terminate()
		return food
	else:
		return newFood(player)
def terminate():
	writeHighscore()
	pygame.quit()
	quit()
def newFood(player):
	while True:
		x, y = randint(0, WIDTH - CELLWIDTH), randint(0, HEIGHT - CELLHEIGHT)
		if not (x % CELLWIDTH == 0 and y % CELLHEIGHT == 0):
			continue
		for c in player.cells:
			c = c.rect
			xCenter, yCenter = x + CELLWIDTH//2, y + CELLHEIGHT//2
			if isPointInsideRect(xCenter,yCenter , c):
				print("Food born in the snake! Ignoring~")
				return newFood(player)
		a, b = CELLWIDTH, CELLHEIGHT
		return cell(x, y, a, b, RED)


def game():
	global FPS, HIGHSCORE

	mainClock = pygame.time.Clock()
	screen = pygame.display.set_mode(SIZESCREEN, MODE)
	pygame.display.set_caption("snakeObject")

	player = snake(WIDTH // 2, HEIGHT // 2)
	food = None
	levelUp = 10
	running = pause(screen, 'ENTER: Iniciar', 'ESC: Sair')
	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				return False
			elif event.type == KEYDOWN:
				if event.key == K_UP or event.key == ord('w'):
					keys['UP'] = True
				elif event.key == K_LEFT or event.key == ord('a'):
					keys['LEFT'] = True
				elif event.key == K_DOWN or event.key == ord('s'):
					keys['DOWN'] = True
				elif event.key == K_RIGHT or event.key == ord('d'):
					keys['RIGHT'] = True
				elif event.key == K_ESCAPE:
					x = pause(screen, '  PAUSE', 'ENTER: QUIT')
					if x:
						return True
				elif event.key == K_RETURN:
					return game()
			elif event.type == KEYUP:
					if event.key == K_UP or event.key == ord('w'):
						keys['UP'] = False
					if event.key == K_LEFT or event.key == ord('a'):
						keys['LEFT'] = False
					if event.key == K_DOWN or event.key == ord('s'):
						keys['DOWN'] = False
					if event.key == K_RIGHT or event.key == ord('d'):
						keys['RIGHT'] = False

		#BACKGROUND
		screen.fill(BLACK)

		#SCORE
		score = (len(player.cells) - 2) * FPS
		scoreText = pygame.font.Font('freesansbold.ttf', 15)
		scoreSurf = scoreText.render('Score: %02d   FPS: %d' %(score, FPS), True, WHITE)
		scoreRect = scoreSurf.get_rect()
		scoreRect.midright = (WIDTH - 20, 10)
		screen.blit(scoreSurf, scoreRect)

		if levelUp < len(player.cells):
			levelUp += 5
			FPS += 1
		if score > HIGHSCORE:
			HIGHSCORE = score 

		#PLAYER
		playerControl(player, screen)
		#player.controlUpdate()
		#player.moveSnake()
		#player.draw(screen)

		#FOOD && COLISIONS
		food = foodControl(screen, player, food, score)
					
		pygame.display.update()
		mainClock.tick(FPS)



keys = {'UP':False, 'LEFT':False, 'DOWN':False, 'RIGHT':False} #UP, LEFT, DOWN RIGHT
motion = {'UP':(0, -CELLHEIGHT), 'LEFT':(-CELLWIDTH, 0), 'DOWN':(0, CELLHEIGHT), 'RIGHT':(CELLWIDTH, 0)}

pygame.init()
game()
pygame.quit()
writeHighscore()
quit()
