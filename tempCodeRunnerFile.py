import pygame
import math

pygame.init()

# Window setup
WIDTH, HEIGHT = 1000, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Planet Simulation")

# Colors
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
ORANGE = (255, 165, 0)
PURPLE = (138, 43, 226)
LIGHT_BLUE = (173, 216, 230)

class Planet:
    # Constants
    AU = 149.6e6 * 1000  # in meters
    G = 6.67428e-11  # Gravitational constant
    SCALE = 220 / AU  # Scale for drawing: 1 AU = 100 pixels
    TIMESTEP = 3600 * 24  # One day in seconds

    def __init__(self, name, x, y, radius, mass, color):
        self.name = name  # Planet's name
        self.x = x  # Position in meters
        self.y = y
        self.radius = radius  # Radius for drawing
        self.mass = mass
        self.color = color

        self.sun = False
        self.distance_to_sun = 0
        self.orbit = []
        self.x_vel = 0  # Velocity in meters per second
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        # Draw the orbit path
        if len(self.orbit) > 2:
            updated_orbit = [(point[0] * self.SCALE + WIDTH / 2, point[1] * self.SCALE + HEIGHT / 2) for point in self.orbit]
            pygame.draw.lines(win, self.color, False, updated_orbit, 2)

        # Draw the planet
        pygame.draw.circle(win, self.color, (int(x), int(y)), self.radius)

        # Draw the name and distance to the sun
        if not self.sun:
            distance_text = f"{round(self.distance_to_sun / 1000, 1)} km"
            draw_text(win, self.name, int(x) - 20, int(y) - self.radius - 20)  # Planet name
            draw_text(win, distance_text, int(x) - 30, int(y) - self.radius + 10)  # Distance to the sun

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2  # F = G * m1 * m2 / r^2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y

    def update_position(self, planets):
        total_fx, total_fy = 0, 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        # Update velocity (acceleration = F / m)
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        # Update position based on velocity
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP

        # Save orbit history for drawing
        self.orbit.append((self.x, self.y))

    def draw_gravitational_lines(self, win, planets):
        for planet in planets:
            if planet.sun:
                pygame.draw.line(win, WHITE, (WIDTH / 2, HEIGHT / 2), 
                                 (self.x * self.SCALE + WIDTH / 2, self.y * self.SCALE + HEIGHT / 2), 1)

# Function to draw text
def draw_text(win, text, x, y, color=WHITE, size=20):
    font = pygame.font.SysFont("comicsans", size)
    label = font.render(text, 1, color)
    win.blit(label, (x, y))

# Sidebar to display planet information
def draw_sidebar(win, planet):
    font = pygame.font.SysFont("Arial", 18)
    sidebar_width = 250
    sidebar_bg = pygame.Surface((sidebar_width, HEIGHT))
    sidebar_bg.fill((30, 30, 30))
    win.blit(sidebar_bg, (WIDTH - sidebar_width, 0))

    lines = [
        f"Planet: {planet.name}",
        f"Mass: {planet.mass:.2e} kg",
        f"Distance to Sun: {planet.distance_to_sun/1000:.2f} km",
        f"Velocity: {math.sqrt(planet.x_vel**2 + planet.y_vel**2):.2f} m/s",
    ]

    for i, line in enumerate(lines):
        label = font.render(line, 1, WHITE)
        win.blit(label, (WIDTH - sidebar_width + 10, 20 + i * 20))

# Handle zoom feature using mouse scroll
def handle_zoom(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 4:  # Scroll up
            Planet.SCALE *= 1.1
        if event.button == 5:  # Scroll down
            Planet.SCALE /= 1.1

def main():
    run = True
    clock = pygame.time.Clock()

    # Create the Sun (massive object at the center)
    sun = Planet("Sun", 0, 0, 30, 1.98892 * 10**30, YELLOW)
    sun.sun = True

    # Create planets with initial positions and velocities
    earth = Planet("Earth", -Planet.AU, 0, 16, 5.9742 * 10**24, BLUE)
    earth.y_vel = 29.783 * 1000  # Earth's orbital velocity in m/s

    mars = Planet("Mars", -1.524 * Planet.AU, 0, 12, 6.39 * 10**23, RED)
    mars.y_vel = 24.077 * 1000  # Mars' orbital velocity in m/s

    venus = Planet("Venus", 0.723 * Planet.AU, 0, 14, 4.8685 * 10**24, WHITE)
    venus.y_vel = -35.02 * 1000  # Venus' orbital velocity in m/s (clockwise)

    mercury = Planet("Mercury", 0.387 * Planet.AU, 0, 8, 3.30 * 10**23, GRAY)
    mercury.y_vel = -47.87 * 1000  # Mercury's orbital velocity in m/s (clockwise)

    # Adding Jupiter, Saturn, Uranus, Neptune
    jupiter = Planet("Jupiter", 5.2 * Planet.AU, 0, 20, 1.898 * 10**27, ORANGE)
    jupiter.y_vel = -13.07 * 1000  # Jupiter's orbital velocity in m/s

    saturn = Planet("Saturn", 9.58 * Planet.AU, 0, 18, 5.683 * 10**26, LIGHT_BLUE)
    saturn.y_vel = -9.68 * 1000  # Saturn's orbital velocity in m/s

    uranus = Planet("Uranus", 19.2 * Planet.AU, 0, 16, 8.681 * 10**25, PURPLE)
    uranus.y_vel = -6.8 * 1000  # Uranus' orbital velocity in m/s

    neptune = Planet("Neptune", 30.05 * Planet.AU, 0, 16, 1.024 * 10**26, BLUE)
    neptune.y_vel = -5.43 * 1000  # Neptune's orbital velocity in m/s

    planets = [sun, earth, mars, venus, mercury, jupiter, saturn, uranus, neptune]
    selected_planet = earth  # Default selected planet for the sidebar

    while run:
        clock.tick(60)  # Limit to 60 frames per second
        WINDOW.fill((0, 0, 0))  # Clear the screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            handle_zoom(event)

        # Update and draw each planet
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WINDOW)
            planet.draw_gravitational_lines(WINDOW, planets)

        # Draw sidebar with info on the selected planet
        draw_sidebar(WINDOW, selected_planet)

        pygame.display.update()

    pygame.quit()

main()
