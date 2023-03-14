from solsystemet import *
from gravity import *
import pygame
pygame.init()

screen = pygame.display.set_mode((1000,1000))
pygame.display.set_caption('SIMULERING')


font = pygame.font.SysFont('comicsans',40,bold=True)
font2 = pygame.font.SysFont('georgia', 50, bold=True)
head = font2.render('!!TRYKK FOR Å SIMULERE!!', True, 'BLACK')
surf = font.render('Solsystemet', True, 'white')
button = pygame.Rect(200,450,250,120)
surf2 = font.render('Gravitytest', True, 'white')
button2 = pygame.Rect(550, 450, 250, 120)


def mainprog():
    while True:
        screen.fill('red')
        screen.blit(head, (125, 300))
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
            if events.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(events.pos):
                    main()
                if button2.collidepoint(events.pos):
                    main2()
        a,b = pygame.mouse.get_pos()
        pygame.draw.rect(screen, (110,110,110),button)
        pygame.draw.rect(screen,(110,110,110),button2)
        if button.x <= a <= button.x + 250 and button.y <= b <= button.y + 120:
            pygame.draw.rect(screen,(180,180,180),button)
        if button2.x <= a <= button2.x + 250 and button2.y <= b <= button2.y + 120:
            pygame.draw.rect(screen,(180,180,180),button2)
    #     else:
    #         pygame.draw.rect(screen, (110,110,110),button)
    #         pygame.draw.rect(screen,(110,110,110),button2)
        screen.blit(surf,(button.x +10, button.y+23))
        screen.blit(surf2,(button2.x +15, button2.y+23))
        pygame.display.update()

mainprog()