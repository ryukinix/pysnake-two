#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Python Studies; Manoel Vilela; 29/01/2015
#
#Snake Game Clone with Pygame
#
#Testing concepts of OO
#Contact: manoel_vilela@engineer.com

from pygame.locals import *
import pygame, time, os, sys
from time import localtime
from random import randint, choice
from itertools import chain

#CONFIGURATION START
WIDTH, HEIGHT = 600, 600; SIZESCREEN = WIDTH, HEIGHT; FPS = 10; MODE = 0; HIGHSCORE = 0; 
COLISIONSCREEN = False; COLISIONPARTNER = False

#CELL
SIZECELL = 20
CELLWIDTH = WIDTH // SIZECELL
CELLHEIGHT = HEIGHT // SIZECELL

#CORS
RED = (255, 0, 0); GREEN = (0, 255, 0); BLUE = (0, 0, 255);  BLACK = (0, 0, 0); WHITE = (255, 255, 255)

#MOTION SNAKE
MOTION = {'UP':(0, -CELLHEIGHT), 
		  'LEFT':(-CELLWIDTH, 0),
		  'DOWN':(0, CELLHEIGHT),
		  'RIGHT':(CELLWIDTH, 0),
}

#CONTROL KEYS
PLAYER1KEYS = {'UP':K_UP, 
			   'LEFT':K_LEFT,
			   'DOWN':K_DOWN,
			   'RIGHT':K_RIGHT,
}
PLAYER2KEYS = {'UP':ord('w'),
			   'LEFT':ord('a'),
			   'DOWN':ord('s'),
			   'RIGHT':ord('d'),
}

#Usado para rotacionar os sprites de acordo com os movimentos
ANGLEMOTION = {'UP':90,
			   'LEFT':180,
			   'DOWN':270,
			   'RIGHT':0,
			   'UPLEFT':(False, -90), #inverse Y and angle change #essas keys abaixo são usadas para controlar os sprites de dobra da cobra
			   'UPRIGHT':(True, -90),
			   'LEFTUP':(True, 0),
			   'LEFTDOWN':(False, 0),
			   'DOWNLEFT':(True, 90),
			   'DOWNRIGHT':(False, 90),
			   'RIGHTUP':(False, 180),
			   'RIGHTDOWN':(True, 180),
}


class cell(object):
	def __init__ (self, x, y, a, b, color = BLUE,  angle = 0):
		self.x = x
		self.y = y
		self.color = color
		self.width = a
		self.height = b
		self.rect = pygame.Rect(x, y, a, b)
		self.angle = angle
		self.pointed = False, None
	def move(self, position):
		self.x, self.y = position
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
	def draw(self, screen):
		color = self.color
		pygame.draw.rect(screen, color, self.rect)
class food(cell):
	def __init__(self, x, y, a, b, color, sprite):
		super(food, self).__init__(x, y, a, b, color)
		self.sprite = sprite
	def drawSprite(self, screen, sprite):
		sprite = self.sprite
		screen.blit(sprite, self.rect)
class snake(cell):
	global MOTION
	def __init__(self, x, y, sprites, color = BLUE, name = 'Snake', move = 'DOWN', a = CELLWIDTH, b = CELLHEIGHT ):
		head = cell(x, y, a, b, color) 
		tail = cell(x, (y + a), a, b, color)
		self.name = name
		self.color = color
		self.cells = [head, tail]
		self.keys = {'UP':False, 'LEFT':False, 'DOWN':False, 'RIGHT':False} #UP, LEFT, DOWN RIGHT
		self.move = MOTION[move]
		self.direction = move
		self.change = ANGLEMOTION[move]
		self.points = [(head.x, head.y, None)]
		self.curve = None
		self.sprites = sprites
	def controlUpdate(self):
		keys = self.keys
		for direction in keys.keys():
			if keys[direction] == True:
				if self.move != MOTION[direction]:
					for a, b in [('UP', 'DOWN'), ('DOWN', 'UP'), ('LEFT', 'RIGHT'), ('RIGHT', 'LEFT')]:
						if self.move == MOTION[a] and direction == b:
							return None
					self.curve = self.direction + direction
					self.change = ANGLEMOTION[direction]
					pointCoord = (self.cells[0].x, self.cells[0].y, self.curve)
					self.points.append(pointCoord) #ponto de dobra
				self.move = MOTION[direction] #UP, LEFT, DOWN RIGHT
				self.direction = direction
				break
	def moveSnake(self):
		dx, dy = self.move
		head = self.cells[0]
		beforeCell = head.x, head.y
		x, y = beforeCell
		x += dx
		y += dy
		
		#Movimentar cabeça
		for xPoint, yPoint, c in self.points:
			if beforeCell == (xPoint, yPoint):
				head.angle = self.change #ângulo 
		head.move((x, y))

		#body and tail follow the head
		snake = self.cells
		snakeLenght = len(self.cells)
		i = 1
		while i < snakeLenght:
			cell = snake[i]
			lastCoord = cell.x, cell.y
			cell.pointed = False, None
			for x, y, curve in self.points:
				if beforeCell == (x, y):
					cellBefore = snake[i - 1]
					cell.angle = cellBefore.angle
					cell.pointed = True, curve
					if cell == snake[-1]: #limpar pontos que já foram atravessados por todas as celulas
						self.points.remove((x, y, curve))
						cell.pointed = False, None
					break					
			cell.move(beforeCell)
			beforeCell = lastCoord
			i +=  1			
			
	def colisionScreen(self, colision = True, xsize = WIDTH, ysize = HEIGHT):
		x_lim, y_lim = xsize - CELLWIDTH, ysize - CELLHEIGHT
		head = self.cells[0]
		x, y = head.x, head.y
		if x > x_lim or x < 0:
			if not colision:
				if x > x_lim:
					self.cells[0].move((0, y))
				else:
					self.cells[0].move((x_lim, y))
			else:
				return True
		if y > y_lim or y < 0:
			if not colision:
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
			newCell = cell(x, y, a, b, self.color, self.change)
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
	def drawSprites(self, screen):
		sprites = self.sprites
		cells = self.cells
		headCell, tailCell = cells[0], cells[-1]
		headAngle, tailAngle = headCell.angle, tailCell.angle
		headRect, tailRect =  headCell.rect, tailCell.rect
		headSprite, tailSprite = sprites[0], sprites[2]
								  #^head      #^tail
		headSprite = pygame.transform.rotate(headSprite, headAngle)
		tailSprite = pygame.transform.rotate(tailSprite, tailAngle)

		screen.blit(headSprite,headRect)
		screen.blit(tailSprite,tailRect)
		if len(cells) > 2:
			for cell in cells[1:-1]:				
				if cell.pointed[0] == True:
					curve = cell.pointed[1]
					bodySprite = sprites[3] #ponto de dobra
					yInverse, bodyAngle = ANGLEMOTION[curve]
					if yInverse:
						bodySprite = pygame.transform.flip(bodySprite, False, yInverse) #era pra ser a coordenada x pra ser invertida, mas loucamente não é.
				else:
					bodySprite = sprites[1] #corpo
					bodyAngle = cell.angle
				bodyRect = cell.rect
				bodySpriteChanged = pygame.transform.rotate(bodySprite, bodyAngle)
				screen.blit(bodySpriteChanged, bodyRect)

			



def isPointInsideRect(x, y, rect):
	if (x > rect.left) and (x < rect.right) and (y > rect.top) and (y < rect.bottom):
		return True
	else:
		return False

def playerDraw(screen, snake):
	snake.controlUpdate()
	snake.moveSnake()
	snake.drawSprites(screen)
			
def newFood(players, sprite):
	while True:
		p1, p2 = players
		x, y = randint(0, WIDTH - CELLWIDTH), randint(0, HEIGHT - CELLHEIGHT)
		if not (x % CELLWIDTH == 0 and y % CELLHEIGHT == 0):
			continue
		for c in chain(p1.cells, p1.cells):
			c = c.rect
			xCenter, yCenter = x + CELLWIDTH//2, y + CELLHEIGHT//2
			if isPointInsideRect(xCenter,yCenter , c):
				sys.stdout.write("Food born in the snake! Ignoring~")
				return newFood(players, sprite)
		a, b = CELLWIDTH, CELLHEIGHT
		return food(x, y, a, b, RED, sprite)

def foodColision(screen, player, players, food, sprite):
	if food != None:
		food.drawSprite(screen, sprite)
		if player.foodColision(food.rect) == True:
			soundPickUp()
			return None
		return food
	else:
		return newFood(players, sprite)	

def deathColision(screen, player, players):
	if player.selfColision() or player.colisionScreen(COLISIONSCREEN):
		return gameOver(screen, player.name, players)
	else:
		if COLISIONPARTNER:
			state =	snakeColision(players)
			if state[0] == True:
				killer = state[1]
				return gameOver(screen, players[killer].name, players)		

def snakeColision(players):
	p1, p2 = players
	cells1, cells2 = p1.cells, p2.cells
	cellsList =	[cells1, cells2]
	head1, head2 = p1.cells[0].rect, p2.cells[0].rect
	(x1, y1), (x2, y2) = head1.center, head2.center
	coordHeads = [(x1, y1), (x2, y2)]
	
	i = 0
	while i < 2:
		x, y = coordHeads[i]
		cells = cellsList[~i]
		for cell in cells[1:]:
			if	isPointInsideRect(x, y, cell.rect):
				sys.stdout.write('Colisão: %s, %s, %s' %(x, y, cell.rect.center) + ' Player%s' %(i + 1))
				return True, i
		i += 1
	return False, i

def score(screen, players, levelUp):
	global FPS, HIGHSCORE
	scores = []
	for player in players:
		foods =  (len(player.cells) - 2)
		score = foods * FPS
		scores.append(score)
		if levelUp < foods:
			playSound('wow')
			levelUp += 5
			FPS += 1

		if score > HIGHSCORE:
			HIGHSCORE = score 
			
	scoreText = pygame.font.Font('freesansbold.ttf', HEIGHT // 20)
	scoreSurf = scoreText.render('Scores     P1: %02d | P2: %02d   FPS: %d' %(scores[0], scores[1], FPS), True, WHITE)
	scoreRect = scoreSurf.get_rect()
	scoreRect.midright = (WIDTH - 40, HEIGHT // 20)
	screen.blit(scoreSurf, scoreRect)

	return levelUp

def terminate():
	writeHighscore()
	pygame.quit()
	exit()

def writeHighscore():
	with open('highscore.txt', 'rw') as rankdb:
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
				if score.isdigit():
					score = int(score)
					scores.append(score)

		sys.stdout.write("HIGHSCORES:\n")
		sys.stdout.write(beforeData)
		write = True
		if len(scores) > 0:
			if HIGHSCORE > max(scores):
				write = True
			else:
				write = False
		if write:
			string = "%4d %s\n" %(HIGHSCORE, time)
			w = rankdb.write(string)
			sys.stdout.write(string)
			sys.stdout.write("Novo HIGHSCORE! %d" %HIGHSCORE)

def controlInput(player, event, control): #De todas, acho que essa é a função mais concisa.
	for typeEvent, state in [(KEYDOWN, True), (KEYUP, False)]:
		if event.type == typeEvent:
			for key in control.keys():
				if event.key == control[key]:
					player.keys[key] = state 

def pause(screen, mensagens, size = HEIGHT // 15, lineSpace = HEIGHT // 15):
	screen.fill(BLACK)
	#TitleGame
	title = pygame.font.Font('freesansbold.ttf', HEIGHT // 15)
	titleSurf = title.render("SnakeGame", True, WHITE)
	titleRect = titleSurf.get_rect()
	titleRect.midright = (int(WIDTH * 3/4 - 20), HEIGHT // 10)
	screen.blit(titleSurf, titleRect)
	
	y = HEIGHT // 2
	for mensagem in mensagens:
		message = pygame.font.Font('freesansbold.ttf', size)
		messageSurf = message.render(mensagem, True, WHITE)
		messageRect = messageSurf.get_rect()
		messageRect.midleft = (int(WIDTH* 1/4), y)
		screen.blit(messageSurf, messageRect)
		y += lineSpace

	clock = pygame.time.Clock()
	while True:
		for event in pygame.event.get():
			if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
				return terminate()
			elif event.type == KEYDOWN and event.key == K_RETURN:
				return True
		pygame.display.update()
		clock.tick(FPS)

def lineOverDraw(screen, x = WIDTH, y = HEIGHT):
	points = [(0, 0), (0, y), (x, y), (x, 0), (0, 0)]
	i = 0
	while i < 4:
		p1, p2 = points[i], points[i+1]
		pygame.draw.line(screen, RED, p1, p2, 5)
		i += 1

def gameOver(screen, playerName, players):
	global FPS
	scores = []
	for player in players:
		score = (len(player.cells) - 2)* FPS
		scores.append(score)
	p1, p2 = scores[0], scores[1]
	if p1 > p2:
		winner = 'Winner: Player1!'
	elif p2 > p1:
		winner = 'Winner: Player2'
	else:
		winner = 'Draw Game!'

	selfKiller = playerName
	playSound('insults')
	question = pause(screen,
					['GameOver',
					 '%s Kill Us'%selfKiller,
					 '',
					 '%s' %winner,
					 '',
					 'P1: %d' %p1,
					 'P2: %d' %p2],
					 30, 40)
	if question:
		return game()
	else:
		return terminate()
def musicPlay():
	try:
		musics = os.listdir('musics')
		music = choice(musics)
		pygame.mixer.music.load('musics' + '/' + music)
		pygame.mixer.music.play(0, 0.0)
	except pygame.error:
		sys.stdout.write('Pygame Error in read the sound: %s' %music)
		return musicPlay()
def soundPickUp():
	sound = pygame.mixer.Sound('pickup.wav')
	sound.play()
def playSound(path):
	sounds = os.listdir(path)
	sound = choice(sounds)
	sound = pygame.mixer.Sound(path + '/' + sound)
	sound.play()

def game():
	global FPS, HIGHSCORE

	pygame.init()
	musicPlay()
	mainClock = pygame.time.Clock()
	screen = pygame.display.set_mode(SIZESCREEN, MODE)
	pygame.display.set_caption("TwoSnakes")
	icon = pygame.image.load('snake.png')
	iconScaled = pygame.transform.scale(icon, (32, 32))
	pygame.display.set_icon(iconScaled)

	
	playerSprites = []
	for color in ['white', 'green']:
		sprites = []; path = 'sprites/%s/' %color
		for image in ['head.png', 'body.png', 'tail.png', 'turn.png']:
			sprite = pygame.image.load(path+image)
			spriteScaled = pygame.transform.scale(sprite, (CELLWIDTH, CELLHEIGHT))
			spriteScaled = pygame.transform.rotate(spriteScaled, 90)
			sprites.append(spriteScaled)
		playerSprites.append(sprites)

	player1 = snake(0, 0, playerSprites[0], BLUE, 'Player1')
	player2 = snake(HEIGHT - CELLWIDTH, 0, playerSprites[1], GREEN, 'Player2')
	players = [player1, player2]

	foodSprite = pygame.image.load('sprites/green/food.png')
	foodSprite = pygame.transform.scale(foodSprite, (CELLWIDTH, CELLHEIGHT))

	food = None;	levelUp = 10
	
	running = pause(screen, ['ENTER: START', 'ESC: QUIT'])

	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				return terminate()
			elif event.type == KEYDOWN:
				if event.key == K_F1:
					FPS += 1
				elif event.key == K_F2:
					FPS -= 1
				elif event.key == K_F5:
					musicPlay() 
				elif event.key == K_ESCAPE:
					pause(screen, ['PAUSE', 'ENTER: CONTINUE', 'ESC: QUIT'])
				elif event.key == K_RETURN:
					return game()
				if FPS <= 0:
					FPS = 1

			controlInput(player1, event, PLAYER1KEYS)
			controlInput(player2, event, PLAYER2KEYS)

		#BACKGROUND
		screen.fill(BLACK)
		for player in players:
			#FOOD
			food = foodColision(screen, player, players, food, foodSprite)
			#PLAYER
			playerDraw(screen, player)
			#COLISION
			deathColision(screen, player, players)
		#SCORE
		levelUp = score(screen, players, levelUp)

		lineOverDraw(screen)

		
		if not pygame.mixer.music.get_busy():
			musicPlay()
		pygame.display.update()
		mainClock.tick(FPS)

if __name__ == '__main__':
	game()

