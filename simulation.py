import pygame   # This is the library used for creating and managing the game window, handling events, and rendering graphics.
import math
pygame.init()

WIDTH, HEIGHT = 800, 800

YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)  
RED = (188, 39, 50)     
WHITE = (255, 255, 255)
GRAY = (169, 169, 169) 

WINDOW = pygame.display.set_mode((800, 800)) # a window of size 800x800 pixels for displaying the simulation
pygame.display.set_caption("Planet Simulation")


class Planet():

    # Constants
    AU = 149.6e6 * 1000 # in metres
    G = 6.67428e-11
    SCALE = 220/AU # 1 AU = 100 pixels
    TIMESTEP = 3600*24 # 1 day of planet at a time

    def __init__(self, x, y, radius, mass, color):
        
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.color = color

        self.sun = False
        self.distance_to_sun = 0
        self.orbit = []

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x*self.SCALE + WIDTH/2;
        y = self.y*self.SCALE + HEIGHT/2;
        
        pygame.draw.circle(win, self.color, (x, y), self.radius)


def main():
    
    run = True
    clock =  pygame.time.Clock(); # The clock object allows you to manage the timing in your game loop by measuring 
                                  # how much time has passed and controlling the speed at which the game updates.
    
    # Sun
    sun = Planet(0, 0, 30, 1.98892 * 10**30, YELLOW)
    sun.sun = True

    # Earth
    earth = Planet(-Planet.AU, 0, 16, 5.9742 * 10**24, BLUE) # Earthy is 1 AU away from the sun
    earth.y_vel = 29.783 * 1000  

    # Mars
    mars = Planet(-1.524 * Planet.AU, 0, 12, 6.39 * 10**23, RED)
    mars.y_vel = 24.077 * 1000  
    
    # Venus
    venus = Planet(0.723 * Planet.AU, 0, 14, 4.8685 * 10**24, WHITE)
    venus.y_vel = 35.02 * 1000  # Venus velocity in m/s (around 35.02 km/s)

    # Mercury
    mercury = Planet(-0.387 * Planet.AU, 0, 8, 3.30 * 10**23, GRAY)
    mercury.y_vel = 47.87 * 1000  # Mercury velocity in m/s (around 47.87 km/s)

    
    planets = [sun, earth, mars, venus, mercury]                            

    while run:
        clock.tick(60)   # no matter how fast the computer is, the game will only run up to 60 frames per second.
        
        for event in pygame.event.get():  # Gives a list of all the events (like keyboard presses, mouse movements, or window closing) that Pygame has detected.
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.draw(WINDOW)    

        pygame.display.update()        

    pygame.quit()


main()                