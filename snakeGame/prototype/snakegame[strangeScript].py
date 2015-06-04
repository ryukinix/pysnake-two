import pygame
import random
import os

pygame.init()

class Worm:
    def __init__(self, surface):
        self.surface = surface
        self.x = surface.get_width() / 2
        self.y = surface.get_height() / 2
        self.length = 1
        self.grow_to = 50
        self.vx = 0
        self.vy = -1
        self.body = []
        self.crashed = False
        self.color = 255, 255, 0

    def event(self, event):
        if event.key == pygame.K_UP:
            if self.vy != 1:
                self.vx = 0
                self.vy = -1
            else:
                a = 1
        elif event.key == pygame.K_DOWN:
            if self.vy != -1:
                self.vx = 0
                self.vy = 1
            else:
                a = 1
        elif event.key == pygame.K_LEFT:
            if self.vx != 1:
                self.vx = -1
                self.vy = 0
            else:
                a = 1
        elif event.key == pygame.K_RIGHT:
            if self.vx != -1:
                self.vx = 1
                self.vy = 0
            else:
                a = 1

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if (self.x, self.y) in self.body:
            self.crashed = True
        self.body.insert(0, (self.x, self.y))
        if (self.grow_to > self.length):
            self.length += 1
        if len(self.body) > self.length:
            self.body.pop()

    def draw(self):
        x, y = self.body[0]
        self.surface.set_at((int(x), int(y)), self.color)
        x, y = self.body[-1]
        self.surface.set_at((int(x), int(y)), (0, 0, 0))

    def position(self):
        return self.x, self.y

    def eat(self):
        self.grow_to += 25

class Food:
    def __init__(self, surface):
        self.surface = surface
        self.x = random.randint(10, surface.get_width()-10)
        self.y = random.randint(10, surface.get_height()-10)
        self.color = 255, 255, 255

    def draw(self):
        pygame.draw.rect(self.surface, self.color, (self.x, self.y, 3, 3), 0)

    def erase(self):
        pygame.draw.rect(self.surface, (0, 0, 0), (self.x, self.y, 3, 3), 0)

    def check(self, x, y):
        if x < self.x or x > self.x +3:
            return False
        elif y < self.y or y > self.y +3:
            return False
        else:
            return True

    def position(self):
        return self.x, self.y

font = pygame.font.Font(None, 25)
GameName = font.render("Worm Eats Dots", True, (255, 255, 0))
GameStart = font.render("Press Any Key to Play", True, (255, 255, 0))

w = 500
h = 500
screen = pygame.display.set_mode((w, h))


GameLoop = True
while GameLoop:
    MenuLoop = True
    while MenuLoop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                MenuLoop = False
        screen.blit(GameName, (180, 100))
        screen.blit(GameStart, (155, 225))
        pygame.display.flip()

    screen.fill((0, 0, 0))
    clock = pygame.time.Clock()
    score = 0
    worm = Worm(screen)
    food = Food(screen)
    running = True

    while running:
        worm.move()
        worm.draw()
        food.draw()

        if worm.crashed:
            running = False
        elif worm.x <= 0 or worm.x >= w-1:
            running = False
        elif worm.y <= 0 or worm.y >= h-1:
            running = False
        elif food.check(worm.x, worm.y):
            score += 1
            worm.eat()
            print ("Score %d" % score)
            food.erase()
            food = Food(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                worm.event(event)

        pygame.display.flip()
        clock.tick(200)

    if not os.path.exists("High Score.txt"):
        fileObject = open("High Score.txt", "w+")
        highscore = 0
    else:
        fileObject = open("High Score.txt", "r+")
        fileObject.seek(0, 0)
        highscore = int(fileObject.read(2))
    if highscore > score:
        a = 1
    else:
        fileObject.seek(0, 0)
        if score < 10:
            fileObject.write("0"+str(score))
        else:
            fileObject.write(str(score))
        highscore = score
    fileObject.close()
    screen.fill((0, 0, 0))
    ScoreBoarda = font.render(("You Scored: "+str(score)), True, (255, 255, 0))
    if highscore == score:
        ScoreBoardb = font.render("NEW HIGHSCORE!", True, (255, 255, 0))
        newscore = 1
    else:
        ScoreBoardb = font.render(("High Score: "+str(highscore)), True, (255, 255, 0))
        newscore = 0
    Again = font.render("Again?", True, (255, 255, 0))
    GameOver = font.render("Game Over!", True, (255, 255, 0))
    screen.blit(GameName, (180, 100))
    screen.blit(GameOver, (200, 137))
    screen.blit(ScoreBoarda, (190, 205))
    if newscore == 0:
        screen.blit(ScoreBoardb, (190, 235))
    elif newscore == 1:
        screen.blit(ScoreBoardb, (175, 235))
    screen.blit(Again, (220, 365))
    pygame.draw.rect(screen, (0, 255, 0), (200, 400, 40, 40), 0)
    pygame.draw.rect(screen, (255, 0, 0), (260, 400, 40, 40), 0)
    LEFT = font.render("L", True, (0, 0, 0))
    RIGHT = font.render("R", True, (0, 0, 0))
    screen.blit(LEFT, (215, 415))
    screen.blit(RIGHT, (275, 415))
    pygame.display.flip()
    loop = True
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x > 200 and x < 240 and y > 400 and y < 440:
                    loop = False
                elif x > 260 and x < 300 and y > 400 and y < 440:
                    GameLoop = False
                    loop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    loop = False
                elif event.key == pygame.K_RIGHT:
                    GameLoop = False
                    loop = False

    screen.fill((0, 0, 0))
pygame.quit()