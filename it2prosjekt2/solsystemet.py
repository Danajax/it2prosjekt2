import pygame
import math 
import csv

pygame.init()

WIDTH, HEIGHT = 1000, 1000 
GD = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solsystemet")


#Henter informasjon fra data.csv og getdatanasa.py
speedvals, distvals = [], []
with open('data.csv', 'r') as file:
    data = csv.reader(file)
    for row in data:
        speedvals.append(float(row[0]))
        distvals.append(float(row[1]))
        
file.close()


#estetikk
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
FONT = pygame.font.SysFont("comicsans", 16)
bg = pygame.image.load('solsys.png')

#definerer en klasse for alle planeter
class Body:
    AU = 149.6e6 * 1000 #meter
    G = 6.67428e-11
    SCALE = 250 / AU #1 AU representerer 100 pixels
    dt = 3600 * 24 # 1 dag
    
    
    def __init__(self, x, y, radius, color, mass): #bruker si enheter
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        
        self.orbit = []
        self.sun = False 
        self.dist_to_sun = 0
        
        self.vx = 0
        self.vy = 0
        
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)
            

        pygame.draw.circle(win, self.color, (x, y), self.radius)
        if not self.sun:
            dist_text = FONT.render(f"{round(self.dist_to_sun / 1000, 1)}km ... {round(self.vy)} m/s", 1, WHITE)
            win.blit(dist_text, (x - dist_text.get_width()/2, y - dist_text.get_height()/2))
        
    def tiltrek(self, other):
        other_x, other_y = other.x, other.y
        distx = other_x - self.x
        disty = other_y - self.y
        dist = math.sqrt(distx ** 2 + disty ** 2)

        if other.sun:
            self.dist_to_sun = dist

        krft = self.G * self.mass * other.mass / dist**2
        theta = math.atan2(disty, distx)
        krft_x = math.cos(theta) * krft
        krft_y = math.sin(theta) * krft
        return krft_x, krft_y

    def opdt_pos(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.tiltrek(planet)
            total_fx += fx
            total_fy += fy

        self.vx += total_fx / self.mass * self.dt
        self.vy += total_fy / self.mass * self.dt

        self.x += self.vx * self.dt
        self.y += self.vy * self.dt
        self.orbit.append((self.x, self.y))
        
        
#hovedfunksjonen for programmet 
def main():
    run = True
    clock = pygame.time.Clock()
    
    sun = Body(0, 0, 30, YELLOW, 1.98892 *10**30)
    sun.sun = True
    
    mercury = Body(distvals[0]  * Body.AU, 0, 8, DARK_GREY, 0.330 * 10 ** 24)
    mercury.vy = -speedvals[0]
    
    venus = Body(distvals[1] * Body.AU, 0, 14, WHITE, 4.8685 * 10 ** 24)
    venus.vy = -speedvals[1]
    
    earth = Body(-distvals[2] * Body.AU, 0, 16, BLUE, 5.9742 * 10 **24)
    earth.vy = speedvals[2]
    
    mars = Body(-distvals[3] * Body.AU, 0, 12, RED, 6.39 * 10 **23)
    mars.vy = speedvals[3]
    
    planets = [sun, earth, mars, mercury, venus]


    while run:
        clock.tick(60)
        GD.fill((0,0,0))
        GD.blit(bg, (0,0))

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        for planet in planets:
            planet.opdt_pos(planets)
            planet.draw(GD)
            
        pygame.display.update()
    pygame.quit()
    
    
#main()