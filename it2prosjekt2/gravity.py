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
M2 = 10e8

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
        #self.momentum_y = -200
        self.momentum_x = 0 #kan eksperimenteres med og eventuelt bruke events/ bruker input for å justere momentumet
        self.momentum_y = 0 #per nå må det hardkodes
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
def linje(mx, my):
    for i in range(1000):
        x = randrange(-500 + mx, mx + 1000)
        y = my
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


def firkant(mx, my):
    for i in range(1000):
        x = randrange(mx, mx + 200)
        y = randrange(my, my + 200)
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
    restrt = False
    while running:
        mx, my = pygame.mouse.get_pos()
        pressed = pygame.key.get_pressed()
        staticpoint = False
        right_clicking = False
        gamedisp.fill(BLACK)
        keys = pygame.key.get_pressed() 
        
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
                    linje(mx, my)
                if event.key == K_f:
                    firkant(mx, my)
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    Partikkels.clear()
                if event.key == pygame.K_DOWN:
                    for l in Partikkels:
                        l.momentum_y += 100
                if event.key == pygame.K_RIGHT:
                    for l in Partikkels:
                        l.momentum_x += 100
                if event.key == pygame.K_LEFT:
                    for l in Partikkels:
                        l.momentum_x += -100
                if event.key == pygame.K_UP:
                    for l in Partikkels:
                        l.momentum_y += -100
                if event.key == pygame.K_a:
                    for l in Partikkels:
                        l.dt *= 10
                if event.key == pygame.K_d:
                    for l in Partikkels:
                        l.dt /= 10
                        
            if keys[pygame.K_g]:
                staticpoint = True
                
            
                

        if staticpoint == False:
            draw2()
            central_mass = pygame.draw.circle(gamedisp, RED, (mx, my), r0)
        else:
            draw(mx, my)
        central_mass = pygame.draw.circle(gamedisp, WHITE, CENTER, r0)
    
        draw2()

        pygame.display.update()
        
            
    pygame.display.quit()
    return restrt

    

    
    
#main2()