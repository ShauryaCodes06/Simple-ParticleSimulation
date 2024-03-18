import pygame as pg 
import random 
import math


''' Basic Variables And Game Window Initialization'''

width, height = 800, 800                       
win = pg.display.set_mode((width, height)) 
pg.display.set_caption("Particle Simulation")
particle_radius = 3 
particle_mass = 1
clock = pg.time.Clock() 
no_of_particles = 100
fps = 60 
G = 10
temperature = 273           # Temperature (in Kelvins [K])
factor = 7 * 1/273
speed_limit = temperature * factor  # Adding a speed limit so particles dont break, also so that max speed changes with temperature

class Particle: 
    def __init__(self, mass, pos, vel_x, vel_y):  # Initialization Of Particles Class
        self.mass = mass 
        self.pos = pos 
        self.vel_x = vel_x 
        self.vel_y = vel_y 

    def get_color(self):        # Function for changing the color of particle according to it's speed
        velocity_magnitude = math.sqrt(self.vel_x ** 2 + self.vel_y ** 2)
        max_velocity = speed_limit
        min_velocity = 0
        normalized_velocity = (velocity_magnitude - min_velocity) / (max_velocity - min_velocity)
        r = int(255 * normalized_velocity)
        b = int(255 * (1 - normalized_velocity))
        color = (r,0,b)
        return color

    def draw(self): 
        try:            # I have added a Try-Except condition so that particles with undefined behaviour are colored yellow and don't crash the simulation
            pg.draw.circle(win, self.get_color(), tuple(self.pos), particle_radius)
        except:
            pg.draw.circle(win, 'yellow', tuple(self.pos), particle_radius)

    def move(self, particles):      # Movement Function with gravitational forces b/w particles
        for particle in particles:
            if particle != self:
                dist_x = particle.pos[0] - self.pos[0]
                dist_y = particle.pos[1] - self.pos[1]
                distance = math.sqrt(dist_x**2 + dist_y**2)
                force = G * (self.mass * particle.mass) / distance**2

                acc_x = force * dist_x / distance / self.mass
                acc_y = force * dist_y / distance / self.mass

                self.vel_x += acc_x
                self.vel_y += acc_y
                if self.vel_x > speed_limit:
                    self.vel_x = speed_limit
                if self.vel_y > speed_limit:
                    self.vel_y = speed_limit
        self.pos[0] += self.vel_x
        self.pos[1] += self.vel_y
        if self.pos[0] >= width - particle_radius or self.pos[0] <= particle_radius:  # Conditions to bounce particles back once they hit the walls
            self.vel_x = -self.vel_x
        if self.pos[1] >= height - particle_radius or self.pos[1] <= particle_radius:   # Same As Above
            self.vel_y = -self.vel_y

        self.handle_collision(particles)

    def handle_collision(self, particles):      # Function to handle collision b/w particles
        for particle in particles:
            if particle != self:
                dx = particle.pos[0] - self.pos[0]
                dy = particle.pos[1] - self.pos[1]
                distance = math.sqrt(dx**2 + dy**2)
                min_dist = particle_radius * 2
                if distance < min_dist:
                    ux = dx / distance
                    uy = dy / distance
                    vrel_x = particle.vel_x - self.vel_x
                    vrel_y = particle.vel_y - self.vel_y
                    vrel_u = vrel_x * ux + vrel_y * uy
                    if vrel_u < 0:
                        j = -2 * vrel_u / (1 / self.mass + 1 / particle.mass)
                        self.vel_x -= j * ux / self.mass
                        self.vel_y -= j * uy / self.mass
                        particle.vel_x += j * ux / particle.mass
                        particle.vel_y += j * uy / particle.mass

def main(): 
    running = True 
    particles = []
    for j in range(no_of_particles):    # Adding Bunch Of Particles At random locations
        p = Particle(particle_mass, [random.randint(0 + particle_radius, width - particle_radius), random.randint(0 + particle_radius, height - particle_radius)], random.randint(-5,5), random.randint(-5,5)) 
        particles.append(p)
    while running:      # Main game-loop
        clock.tick(fps) 
        win.fill('black') 

        for event in pg.event.get(): 
            if event.type == pg.QUIT: 
                running = False 

        for particle in particles: # Moving and drawing each particle and also iterationg over each of them to calculate gravitational forces
            particle.move(particles)
            particle.draw()

        pg.display.flip() # Updating the display each frame

if __name__ == '__main__': 
    main()
