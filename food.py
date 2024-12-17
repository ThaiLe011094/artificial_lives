import random
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, RED


class Food:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True

    def render(self, surface):
        if self.alive:
            pygame.draw.rect(surface, RED, (self.x, self.y, 5, 5))

    @staticmethod
    def random():
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        return Food(x, y)
