import random
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, RED, ORANGE


class Predator:

    def __init__(self, x, y, size=10, energy=200, speed=10):
        self.x = x
        self.y = y
        self.size = size
        self.energy = energy
        self.speed = speed
        self.alive = True

    def move(self):
        if not self.alive:
            return
        self.x += random.randint(-self.speed, self.speed)
        self.y += random.randint(-self.speed, self.speed)
        self.x = max(0, min(SCREEN_WIDTH, self.x))
        self.y = max(0, min(SCREEN_HEIGHT, self.y))
        self.energy -= 1
        if self.energy <= 0:
            self.alive = False

    def hunt(self, organisms):
        for organism in organisms:
            if organism.alive and abs(self.x - organism.x) < self.size and abs(
                    self.y - organism.y) < self.size:
                organism.alive = False
                self.energy += 50
                self.size += 1

    def render(self, surface):
        if self.alive:
            pygame.draw.circle(surface, ORANGE, (self.x, self.y), self.size)

    @staticmethod
    def random():
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        return Predator(x, y)
