import math
import random
from math import cos, sin, sqrt
from random import randrange
from pygame.locals import *
import pygame

BRED = 1000
HOYD = 1000
CENTER = BRED // 2, HOYD // 2
C_X = BRED // 2
C_Y = HOYD // 2

#fysikk konst 
G = 0.2
M = 10e7
M2 = 10e9

#farger
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

#radius til centremass
r0 = 10


pygame.init()


class Partikkel:
    def __init__(self, x, y):
        self.g = G
        self.mass = 2
        self.x = x
        self.y = y
        #self.momentum_x = 200
        #self.momentum_y = 200
        self.momentum_x = 200 #kan eksperimenteres med og eventuelt bruke events/ bruker input for å justere momentumet
        self.momentum_y = -200 #per nå må det hardkodes
        self.dt = 0.001

    def fysk(self, pos_cmass):
        x2 = pos_cmass[0]
        y2 = pos_cmass[1]
        hyp = (self.x - x2) ** 2 + (self.y - y2) ** 2
        theta = math.atan2(y2 - self.y, x2 - self.x)
        kraft = (self.g * self.mass * M) / hyp
        kraft_x = kraft * math.cos(theta)
        kraft_y = kraft * math.sin(theta)
        self.momentum_x += kraft_x * self.dt
        self.momentum_y += kraft_y * self.dt
        self.x += self.momentum_x / self.mass * self.dt
        self.y += self.momentum_y / self.mass * self.dt
        return [self.x, self.y]
    
    #hovedsakelig for testårsaker
    def fysk2(self, pos_cmass):
        x2 = pos_cmass[0]
        y2 = pos_cmass[1]
        hyp = (self.x - x2) ** 2 + (self.y - y2) ** 2
        theta = math.atan2(y2 - self.y, x2 - self.x)
        kraft = (self.g * self.mass * M2) / hyp
        kraft_x = kraft * math.cos(theta)
        kraft_y = kraft * math.sin(theta)
        self.momentum_x += kraft_x * self.dt
        self.momentum_y += kraft_y * self.dt
        self.x += self.momentum_x / self.mass * self.dt
        self.y += self.momentum_y / self.mass * self.dt
        return [self.x, self.y]


gamedisp = pygame.display.set_mode((BRED, HOYD))

Partikkels = []

r = 100 #radius til sirkel-funksjonen


#lager ulike mønstre for de ulike partiklene
def linje():
    for i in range(1000):
        x = randrange(-500, 1000)
        y = 100
        p = Partikkel(x, y)
        Partikkels.append(p)


def sirkel(mxx, myy):
    for i in range(500):
        ang = random.uniform(0, 1) * 2 * math.pi
        hyp = sqrt(random.uniform(0, 1)) * r
        adj = cos(ang) * hyp
        opp = sin(ang) * hyp
        x = mxx + adj
        y = myy + opp
        p = Partikkel(x, y)
        Partikkels.append(p)


def firkant():
    for i in range(1000):
        x = randrange(400, 700)
        y = randrange(700, 1000)
        p = Partikkel(x, y)
        Partikkels.append(p)

#draw funksjon for å tegne de ulike mønsterne til bruker, hvorav den ene bruker museposisjon, mens den andre har en const x og y
def draw(mxxx, myyy):
    for i in range(len(Partikkels)):
        pygame.draw.circle(gamedisp, WHITE, (Partikkels[i].fysk2((mxxx, myyy))), 1)
        
def draw2():
     for i in range(len(Partikkels)):
        pygame.draw.circle(gamedisp, WHITE, (Partikkels[i].fysk((C_X, C_Y))), 1)

#mainfunksjon for programmet
def main2():
    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        pressed = pygame.key.get_pressed()
        staticpoint = False
        right_clicking = False
        gamedisp.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    sirkel(mx, my)
                if event.button == 3:
                    staticpoint = True
            if event.type == KEYDOWN:
                if event.key == K_l:
                    linje()
                if event.key == K_f:
                    firkant()
                    
                
            #if event.type == MOUSEBUTTONUP:
                #if event.button == 1:

                #if event.button == 3:
                

        if staticpoint == False:
            draw2()
            central_mass = pygame.draw.circle(gamedisp, RED, (mx, my), r0)
        else:
            draw(mx, my)
        
        central_mass = pygame.draw.circle(gamedisp, WHITE, CENTER, r0)
    

        # Gravity point
        #central_mass = pygame.draw.circle(gamedisp, WHITE, CENTER, r0)

        #draw(mx, my)
        draw2()

        pygame.display.update()
        
    pygame.quit()

    
#main2()
