import pygame
import vectors
import random
import math
import linear_solver

class PolygonModel:
    def __init__(self, screen, color, points) -> None:
        self.screen = screen
        self.color = color
        self.points = points
        self.rotation_angle = 0
        self.angular_velocity = 0
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0

    def transformed(self):
        rotated = [vectors.rotate2d(self.rotation_angle, v) for v in self.points]
        return [vectors.add((self.x,self.y),v) for v in rotated]
    def draw_poly(self):
        pixel_points = [to_pixels(x,y) for x,y in self.transformed()]
        pygame.draw.aalines(self.screen, self.color, True, pixel_points, 10)
    def draw_segment(self, color, v1, v2):
        pygame.draw.aalines(self.screen, color, True, [to_pixels(*v1), to_pixels(*v2)], 10)
    def draw(self):    
        self.draw_poly()
    def segments(self):
        count = len(self.points)
        transformed_points = self.transformed()
        return [(transformed_points[i], transformed_points[(i+1) % count]) for i in range(0, count)]
    def intersect_with(self, other_segment) -> bool:
        for seg in self.segments():
            if linear_solver.do_segments_intersect(seg, other_segment):
                return True
        return False
    def collide_with(self, other_polygon) -> bool:
        for other_seg in other_polygon.segments():
            if self.intersect_with(other_seg):
                return True
        return False
    def move(self, milliseconds):
        dx, dy = self.vx * milliseconds / 1000.0, self.vy * milliseconds / 1000.0
        self.x, self.y = vectors.add((self.x,self.y), (dx,dy))
        if self.x < -10:
            self.x += 20
        if self.y < -10:
            self.y += 20
        if self.x > 10:
            self.x -= 20
        if self.y > 10:
            self.y -=20
        self.rotation_angle += self.angular_velocity * milliseconds / 1000.0

class Ship(PolygonModel):
    def __init__(self, screen) -> None:
        super().__init__(screen, "green", [(0.5,0), (-0.25,0.25), (-0.25,-0.25)])
    
    def laser_segment(self) -> ((float, float),(float, float)):
        dist = 40
        x, y = self.transformed()[0]
        return ((x, y), 
                (x + dist * math.cos(self.rotation_angle), 
                 y + dist * math.sin(self.rotation_angle)))
    
    def shot(self) -> None:
        laser = self.laser_segment()
        self.draw_segment("red", *laser)

class Asteroid(PolygonModel):
    def __init__(self, screen) -> None:
        sides = random.randint(5, 9)
        vs = [vectors.to_cartesian((random.uniform(0.5, 1.0), 2 * math.pi * i /sides)) for i in range(0, sides)]
        super().__init__(screen, "green", vs)
        self.x = random.randint(-9, 9)
        self.y = random.randint(-9, 9)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.angular_velocity = random.uniform(-math.pi/2,math.pi/2)

width, height = 400, 400

def to_pixels(x,y):
    return (width/2 + width * x / 20, height/2 - height * y / 20)

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

def run():
    pygame.init()
    screen = pygame.display.set_mode([width,height])
    pygame.display.set_caption("Asteroids")

    done = False
    clock = pygame.time.Clock()

    ship = Ship(screen)
    asteroid_count = 10
    asteroids = [Asteroid(screen) for _ in range(0, asteroid_count)]
    acceleration = 3
    while not done:
        screen.fill("black")
        clock.tick()
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop 
        keys = pygame.key.get_pressed()
        milliseconds = clock.get_time()
        if keys[pygame.K_LEFT]:
            ship.rotation_angle += milliseconds * (2*math.pi / 1000)
        if keys[pygame.K_RIGHT]:
            ship.rotation_angle -= milliseconds * (2*math.pi / 1000)
        if keys[pygame.K_UP]:
            ax = acceleration * math.cos(ship.rotation_angle)
            ay = acceleration * math.sin(ship.rotation_angle)
            ship.vx += ax * milliseconds/1000
            ship.vy += ay * milliseconds/1000

        elif keys[pygame.K_DOWN]:
            ax = - acceleration * math.cos(ship.rotation_angle)
            ay = - acceleration * math.sin(ship.rotation_angle)
            ship.vx += ax * milliseconds/1000
            ship.vy += ay * milliseconds/1000

        if keys[pygame.K_SPACE]:
            ship.shot()
            laser = ship.laser_segment()
            for asteroid in asteroids:
                if asteroid.intersect_with(laser):
                    asteroids.remove(asteroid)

        ship.move(milliseconds)
        ship.draw()
        for asteroid in asteroids:
            asteroid.move(milliseconds)
            asteroid.draw()

        for asteroid in asteroids:
            if asteroid.collide_with(ship):
                done = True

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    run()