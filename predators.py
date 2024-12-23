import math
import random
import pygame
# from config import ORANGE, SCREEN_WIDTH, SCREEN_HEIGHT
import config
import string

class Predator:
    def __init__(
            self,
            x,
            y,
            size=config.PREDATOR_SIZE,
            energy=config.PREDATOR_BASE_ENERGY,
            speed=config.PREDATOR_SPD,
            starvation_threshold=config.PREDATOR_STARVATION_THRESHOLD):
        self.x = x
        self.y = y
        self.size = size
        self.energy = energy
        self.speed = speed
        self.alive = True
        self.starvation_threshold = starvation_threshold
        self.name = ''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits)
            for _ in range(config.NUMBER_OF_NAME_CHAR))

    def move(self, organisms):
        if not self.alive:
            return

        # If starving, move toward the nearest organism
        if self.energy <= self.starvation_threshold:
            closest_organism = self.find_closest_organism(organisms)
            if closest_organism:
                self.move_toward(closest_organism.x, closest_organism.y)
        else:
            # Free movement
            self.x += random.randint(-self.speed, self.speed)
            self.y += random.randint(-self.speed, self.speed)

        # Keep within screen bounds
        self.x = max(0, min(config.SCREEN_WIDTH, self.x))
        self.y = max(0, min(config.SCREEN_HEIGHT, self.y))

        # Decrease energy due to movement
        self.energy -= config.PREDATOR_ENERGY_DEPLETE_RATE
        if self.energy <= 0:
            self.alive = False
        print(f"predator {self.name}:", self.energy)

    def find_closest_organism(self, organisms):
        closest_organism = None
        min_distance = float('inf')
        for organism in organisms:
            if organism.alive:
                distance = math.sqrt((self.x - organism.x) ** 2 + (self.y - organism.y) ** 2)
                if distance < min_distance:
                    closest_organism = organism
                    min_distance = distance
        return closest_organism

    def move_toward(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            self.x += self.speed * (dx / distance)
            self.y += self.speed * (dy / distance)

    def hunt(self, organisms):
        if not self.alive:
            return
        for organism in organisms:
            distance = math.sqrt((self.x - organism.x) ** 2 + (self.y - organism.y) ** 2)
            if distance < self.size and self.energy <= self.starvation_threshold:
                organism.alive = False
                self.energy += random.randint(40, 80)

    def get_hitbox(self):
        return pygame.Rect(
            self.x - self.size, self.y - self.size,
            config.PREDATOR_HITBOX_RADIUS, config.PREDATOR_HITBOX_RADIUS)

    def render(self, screen):
        if self.alive:
            pygame.draw.circle(screen, config.ORANGE, (int(self.x), int(self.y)), self.size)
            font = pygame.font.SysFont(None, 24)
            text = font.render(f'{self.name} ({int(self.energy)})', True, (255, 255, 255))
            screen.blit(text, (self.x - self.size, self.y - self.size - 20))

    @staticmethod
    def random():
        x = random.randint(0, config.SCREEN_WIDTH)
        y = random.randint(0, config.SCREEN_HEIGHT)
        return Predator(x, y)
