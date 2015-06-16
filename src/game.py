# -*-  coding: utf-8  -*-
# !/usr/bin/env python

from __future__ import division, print_function
import pygame
import os
from pygame.locals import *
from time import localtime
from random import randint, choice
from itertools import *
from os.path import join

# CONFIGURATION START
WIDTH, HEIGHT = 600, 600
SIZESCREEN = WIDTH, HEIGHT
FPS = 10
MODE_WINDOW = 0
HIGHSCORE = 0
COLISIONSCREEN = False
COLISIONPARTNER = False
# CELL
SIZECELL = 20
CELLWIDTH = WIDTH // SIZECELL
CELLHEIGHT = HEIGHT // SIZECELL

# CORS
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# MOTION SNAKE
MOTION = {
    'UP': (0, -CELLHEIGHT),
    'LEFT': (-CELLWIDTH, 0),
    'DOWN': (0, CELLHEIGHT),
    'RIGHT': (CELLWIDTH, 0)
}

# CONTROL KEYS
PLAYER1KEYS = {
    'UP': K_UP,
    'LEFT': K_LEFT,
    'DOWN': K_DOWN,
    'RIGHT': K_RIGHT
}

PLAYER2KEYS = {
    'UP': ord('w'),
    'LEFT': ord('a'),
    'DOWN': ord('s'),
    'RIGHT': ord('d'),
}

# It's used for rotate the sprites following the direction moves
# The keys below are used for control the snake turn sprites
ANGLEMOTION = {
    'UP': 90,
    'LEFT': 180,
    'DOWN': 270,
    'RIGHT': 0,
    'UPLEFT': (False, -90),
    'UPRIGHT': (True, -90),
    'LEFTUP': (True, 0),
    'LEFTDOWN': (False, 0),
    'DOWNLEFT': (True, 90),
    'DOWNRIGHT': (False, 90),
    'RIGHTUP': (False, 180),
    'RIGHTDOWN': (True, 180),
}


class cell(object):
    def __init__(self, x, y, a, b, color=BLUE, angle=0):
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
        # A incompatible methods with python 3.x and 2.x [need fixing]
        super(food, self).__init__(x, y, a, b, color)
        self.sprite = sprite

    def draw_sprite(self, screen, sprite):
        sprite = self.sprite
        screen.blit(sprite, self.rect)


class snake(cell):
    global MOTION

    def __init__(self, x, y, sprites, color=BLUE,
                 name='Snake', move='DOWN', a=CELLWIDTH, b=CELLHEIGHT):
        head = cell(x, y, a, b, color)
        tail = cell(x, (y + a), a, b, color)
        self.name = name
        self.color = color
        self.cells = [head, tail]
        self.keys = {'UP': False, 'LEFT': False, 'DOWN': False, 'RIGHT': False}
        self.move = MOTION[move]
        self.direction = move
        self.change = ANGLEMOTION[move]
        self.points = [(head.x, head.y, None)]
        self.curve = None
        self.sprites = sprites

    def control_update(self):
        keys = self.keys
        for direction in keys.keys():
            if keys[direction] == True:
                if self.move != MOTION[direction]:
                    moves = [
                        ('UP', 'DOWN'),
                        ('DOWN', 'UP'),
                        ('LEFT', 'RIGHT'),
                        ('RIGHT', 'LEFT')
                    ]
                    for a, b in moves:
                        if self.move == MOTION[a] and direction == b:
                            return None
                    self.curve = self.direction + direction
                    self.change = ANGLEMOTION[direction]
                    pointCoord = (self.cells[0].x, self.cells[0].y, self.curve)
                    self.points.append(pointCoord)  # ponto de dobra
                self.move = MOTION[direction]  # UP, LEFT, DOWN RIGHT
                self.direction = direction
                break

    def move_snake(self):
        dx, dy = self.move
        head = self.cells[0]
        before_cell = head.x, head.y
        x, y = before_cell
        x += dx
        y += dy

        # move the head
        for x_point, y_point, c in self.points:
            if before_cell == (x_point, y_point):
                head.angle = self.change
        head.move((x, y))

        # body and tail follow the head
        snake = self.cells
        snakeLenght = len(self.cells)
        i = 1
        while i < snakeLenght:
            cell = snake[i]
            last_coord = cell.x, cell.y
            cell.pointed = False, None
            for x, y, curve in self.points:
                if before_cell == (x, y):
                    cellBefore = snake[i - 1]
                    cell.angle = cellBefore.angle
                    cell.pointed = True, curve

                    # clean old points
                    if cell == snake[-1]:
                        self.points.remove((x, y, curve))
                        cell.pointed = False, None
                    break

            cell.move(before_cell)
            before_cell = last_coord
            i += 1

    def colision_screen(self, colision=True, xsize=WIDTH, ysize=HEIGHT):
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

    def food_colision(self, food):
        head = self.cells[0]
        head_rect = head.rect
        x, y = food.center
        if is_point_inside_rect(x, y, head_rect):
            a, b = food.size
            x, y = food.x, food.y
            newCell = cell(x, y, a, b, self.color, self.change)
            self.cells.insert(0, newCell)
            return True
        return False

    def self_colision(self):
        head = self.cells[0].rect
        x, y = head.center
        for c in self.cells[1:]:
            c = c.rect
            if is_point_inside_rect(x, y, c):
                return True
        return False

    def draw(self, screen):
        for c in self.cells:
            c.draw(screen)

    def sprites_draw(self, screen):
        sprites = self.sprites
        cells = self.cells
        head_cell, tailCell = cells[0], cells[-1]
        head_angle, tailAngle = head_cell.angle, tailCell.angle
        head_rect, tailRect = head_cell.rect, tailCell.rect
        head_sprite, tail_sprite = sprites[0], sprites[2]
        head_sprite = pygame.transform.rotate(head_sprite, head_angle)
        tail_sprite = pygame.transform.rotate(tail_sprite, tailAngle)

        screen.blit(head_sprite, head_rect)
        screen.blit(tail_sprite, tailRect)
        if len(cells) > 2:
            for cell in cells[1:-1]:
                if cell.pointed[0] == True:
                    curve = cell.pointed[1]
                    body_sprite = sprites[3]  # snake point-curve
                    yInverse, bodyAngle = ANGLEMOTION[curve]

                    # shoulde be x, but is y. (WTF?)
                    if yInverse:
                        body_sprite = pygame.transform.flip(body_sprite,
                                                            False,
                                                            yInverse)
                else:
                    body_sprite = sprites[1]
                    bodyAngle = cell.angle
                body_rect = cell.rect
                body_spriteChanged = pygame.transform.rotate(body_sprite,
                                                             bodyAngle)
                screen.blit(body_spriteChanged, body_rect)


def is_point_inside_rect(x, y, rect):
    if (x > rect.left) and \
       (x < rect.right) and \
       (y > rect.top) and \
       (y < rect.bottom):
        return True
    else:
        return False


def player_draw(screen, snake):
    snake.control_update()
    snake.move_snake()
    snake.sprites_draw(screen)


def new_food(players, sprite):
    while True:
        p1, p2 = players
        x, y = randint(0, WIDTH - CELLWIDTH), randint(0, HEIGHT - CELLHEIGHT)
        if not (x % CELLWIDTH == 0 and y % CELLHEIGHT == 0):
            continue
        for c in chain(p1.cells, p1.cells):
            c = c.rect
            x_center, y_center = x + CELLWIDTH//2, y + CELLHEIGHT//2
            if is_point_inside_rect(x_center, y_center, c):
                print("Food born in the snake! Ignoring~")
                return new_food(players, sprite)
        a, b = CELLWIDTH, CELLHEIGHT
        return food(x, y, a, b, RED, sprite)


def food_colision(screen, player, players, food, sprite):
    if food is not None:
        food.draw_sprite(screen, sprite)
        if player.food_colision(food.rect) == True:
            sound_pickup()
            return None
        return food
    else:
        return new_food(players, sprite)


def death_colision(screen, player, players):
    if player.self_colision() or player.colision_screen(COLISIONSCREEN):
        return game_over(screen, player.name, players)
    else:
        if COLISIONPARTNER:
            state = snake_colision(players)
            if state[0] == True:
                killer = state[1]
                return game_over(screen, players[killer].name, players)


def snake_colision(players):
    p1, p2 = players
    cells1, cells2 = p1.cells, p2.cells
    cells_list = [cells1, cells2]
    head1, head2 = p1.cells[0].rect, p2.cells[0].rect
    (x1, y1), (x2, y2) = head1.center, head2.center
    coord_heads = [(x1, y1), (x2, y2)]

    i = 0
    while i < 2:
        x, y = coord_heads[i]
        cells = cells_list[~i]
        for cell in cells[1:]:
            if is_point_inside_rect(x, y, cell.rect):
                print('Colisão: ', x, y, cell.rect.center)
                print('Player%s' % (i + 1))
                return True, i
        i += 1
    return (False, i)


def score(screen, players, level_up):
    global FPS, HIGHSCORE
    scores = []
    for player in players:
        foods = (len(player.cells) - 2)
        score = foods * FPS
        scores.append(score)
        if level_up < foods:
            play_sound('wow')
            level_up += 5
            FPS += 1

        if score > HIGHSCORE:
            HIGHSCORE = score

    upmessage = 'Scores     P1: %02d | P2: %02d   FPS: %d' \
                % (scores[0], scores[1], FPS)
    score_text = pygame.font.Font('freesansbold.ttf', HEIGHT // 20)
    score_surf = score_text.render(upmessage, True, WHITE)
    score_rect = score_surf.get_rect()
    score_rect.midright = (WIDTH - 40, HEIGHT // 20)
    screen.blit(score_surf, score_rect)

    return level_up


def terminate():
    write_highscore()
    pygame.quit()
    exit()


def write_highscore():
    with open('highscore.txt', 'rw') as rankdb:
        t = localtime()
        day, month, year = t.tm_mday, t.tm_mon, t.tm_year
        hour, minute, second = t.tm_hour, t.tm_min, t.tm_sec
        time = " | %s:%s:%s %s/%s/%s" \
               % (hour, minute, second, day, month, year)

        data = rankdb.read()
        before_data = data
        data = data.split('\n')
        scores = []

        for line in data:
            for score in line.split('|'):
                score = score.strip()
                if score.isdigit():
                    score = int(score)
                    scores.append(score)

        print("HIGHSCORES:")
        print(before_data, end='')
        write = True
        if len(scores) > 0:
            if HIGHSCORE > max(scores):
                write = True
            else:
                write = False
        if write:
            string = "%4d %s\n" % (HIGHSCORE, time)
            w = rankdb.write(string)
            print(string)
            print("Novo HIGHSCORE! %d" % HIGHSCORE)


# Of all, i think this function is a more beatiful things i done <3
# (newbie-lol)

def controlInput(player, event, control):
    for type_event, state in [(KEYDOWN, True), (KEYUP, False)]:
        if event.type == type_event:
            for key in control.keys():
                if event.key == control[key]:
                    player.keys[key] = state


def pause(screen, mensagens, size=HEIGHT//15, lineSpace=HEIGHT//15):
    screen.fill(BLACK)
    # TitleGame
    title = pygame.font.Font('freesansbold.ttf', HEIGHT // 15)
    title_surf = title.render("SnakeGame", True, WHITE)
    title_rect = title_surf.get_rect()
    title_rect.midright = (int(WIDTH * 3/4 - 20), HEIGHT // 10)
    screen.blit(title_surf, title_rect)

    y = HEIGHT // 2
    for mensagem in mensagens:
        message = pygame.font.Font('freesansbold.ttf', size)
        message_surf = message.render(mensagem, True, WHITE)
        message_rect = message_surf.get_rect()
        message_rect.midleft = (int(WIDTH * 1/4), y)
        screen.blit(message_surf, message_rect)
        y += lineSpace

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or \
               event.type == KEYDOWN and \
               event.key == K_ESCAPE:
                return terminate()

            elif event.type == KEYDOWN:
                if event.key == K_RETURN or \
                   event.key == K_KP_ENTER:
                    return True

        pygame.display.update()
        clock.tick(FPS)


def lineOverDraw(screen, x=WIDTH, y=HEIGHT):
    points = [(0, 0), (0, y), (x, y), (x, 0), (0, 0)]
    i = 0
    while i < 4:
        p1, p2 = points[i], points[i+1]
        pygame.draw.line(screen, RED, p1, p2, 5)
        i += 1


def game_over(screen, playerName, players):
    global FPS
    scores = []
    for player in players:
        score = (len(player.cells) - 2) * FPS
        scores.append(score)
    p1, p2 = scores[0], scores[1]
    if p1 > p2:
        winner = 'Winner: Player1!'
    elif p2 > p1:
        winner = 'Winner: Player2'
    else:
        winner = 'Draw Game!'

    selfKiller = playerName
    play_sound('insults')
    message = [
        'GameOver',
        '%s Kill Us' % selfKiller,
        '',
        '%s' % winner,
        '',
        'P1: %d' % p1,
        'P2: %d' % p2
    ]
    question = pause(screen, message, 30, 40)

    if question:
        return game_world()
    else:
        return terminate()


def music_play():
    try:
        musics = os.listdir('musics')
        music = choice(musics)
        pygame.mixer.music.load(join('musics', music))
        pygame.mixer.music.play(0, 0.0)
    except pygame.error:
        print('Pygame Error in read the sound: %s' % (music))
        return music_play()


def sound_pickup():
    sound = pygame.mixer.Sound('pickup.wav')
    sound.play()


def play_sound(path):
    sounds = os.listdir(path)
    sound = choice(sounds)
    sound = pygame.mixer.Sound(join(path, sound))
    sound.play()


def game_world():
    global FPS, HIGHSCORE

    pygame.init()
    music_play()
    main_clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SIZESCREEN, MODE_WINDOW)
    pygame.display.set_caption("pysnake-two")
    icon = pygame.image.load('snake.png')
    icon_scaled = pygame.transform.scale(icon, (32, 32))
    pygame.display.set_icon(icon_scaled)

    playerSprites = []
    for color in ['white', 'green']:
        sprites = []
        path = "sprites/%s/" % (color)
        for image in ['head.png', 'body.png', 'tail.png', 'turn.png']:
            cell = (CELLWIDTH, CELLHEIGHT)
            sprite = pygame.image.load(join(path, image))
            spriteScaled = pygame.transform.scale(sprite, cell)
            spriteScaled = pygame.transform.rotate(spriteScaled, 90)
            sprites.append(spriteScaled)
        playerSprites.append(sprites)

    player1 = snake(0, 0, playerSprites[0], BLUE, 'Player1')
    player2 = snake(HEIGHT - CELLWIDTH, 0, playerSprites[1], GREEN, 'Player2')
    players = [player1, player2]

    food_sprite = pygame.image.load('sprites/green/food.png')
    food_sprite = pygame.transform.scale(food_sprite, (CELLWIDTH, CELLHEIGHT))

    food = None
    level_up = 10

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
                    music_play()
                elif event.key == K_ESCAPE:
                    pause(screen, ['PAUSE', 'ENTER: CONTINUE', 'ESC: QUIT'])
                elif event.key == K_RETURN:
                    return game_world()
                if FPS <= 0:
                    FPS = 1

            controlInput(player1, event, PLAYER1KEYS)
            controlInput(player2, event, PLAYER2KEYS)

        # BACKGROUND
        screen.fill(BLACK)
        for player in players:
            # FOOD
            food = food_colision(screen, player, players, food, food_sprite)
            # PLAYER
            player_draw(screen, player)
            # COLISION
            death_colision(screen, player, players)
        # SCORE
        level_up = score(screen, players, level_up)

        lineOverDraw(screen)

        if not pygame.mixer.music.get_busy():
            music_play()
        pygame.display.update()
        main_clock.tick(FPS)

if __name__ == '__main__':
    game_world()
