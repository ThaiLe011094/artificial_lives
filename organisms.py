import random
import math
import pygame
# from config import GREEN, SCREEN_WIDTH, SCREEN_HEIGHT
import config
import string
from typing import Final

class Organism:
    def __init__(
            self,
            x,
            y,
            size=config.ORGANISM_SIZE,
            energy=config.ORGANISM_BASE_ENERGY,
            speed=config.ORGANISM_SPD,
            starvation_threshold=config.ORGANISM_STARVATION_THRESHOLD,
            color=config.GREEN
        ):
        self.x = x
        self.y = y
        self.size = size
        self.energy = energy
        self.speed: Final[int] = speed  # Check constant, only works when checking using mypy
        self.alive = True
        self.starvation_threshold = starvation_threshold
        self.color = color
        self.mating_cooldown = 0  # Time until this organism can mate again
        self.name = ''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits)
            for _ in range(config.NUMBER_OF_NAME_CHAR))
        # Randomly choose between two images
        image_path = random.choice(config.ORGANSIM_IMG_PATH)
        self.image = pygame.image.load(image_path)
        self.avatar = pygame.transform.scale(self.image, config.ORGANISM_IMG_SIZE)
        self.previous_x = x  # Store the previous x position

    def move(self, food_items):
        if not self.alive:
            return

        print(f"Moving organism {self.name} at position ({self.x}, {self.y}) with energy {self.energy}")

        # If starving, move toward the nearest food
        if self.energy <= self.starvation_threshold:
            closest_food = self.find_closest_food(food_items)
            if closest_food:
                print(f"Organism {self.name} is starving and moving towards food at ({closest_food.x}, {closest_food.y})")
                self.move_toward(closest_food.x, closest_food.y)
        else:
            # Free movement
            try:
                dx = random.randint(-self.speed, self.speed)
                dy = random.randint(-self.speed, self.speed)
                self.x += dx
                self.y += dy
                print(f"Organism {self.name} moved freely by ({dx}, {dy}) to ({self.x}, {self.y})")
            except Exception as e:
                print(f"Exception occurred for organism {self.name}: {e}")
                raise Exception(f"self.speed: {self.speed}")

        # Keep within screen bounds
        self.x = max(0, min(config.SCREEN_WIDTH, self.x))
        self.y = max(0, min(config.SCREEN_HEIGHT, self.y))
        print(f"Organism {self.name} position adjusted to screen bounds: ({self.x}, {self.y})")

        # Decrease energy due to movement
        self.energy -= 1
        print(f"Organism {self.name} energy decreased to {self.energy}")

        if self.energy <= 0:
            self.alive = False
            print(f"Organism {self.name} has died due to lack of energy")


    def find_closest_food(self, food_items):
        closest_food = None
        min_distance = float('inf')
        for food in food_items:
            if food.alive:
                distance = math.sqrt((self.x - food.x) ** 2 + (self.y - food.y) ** 2)
                if distance < min_distance:
                    closest_food = food
                    min_distance = distance
        return closest_food

    def move_toward(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            self.previous_x = self.x  # Update previous x position
            self.x += self.speed * (dx / distance)
            self.y += self.speed * (dy / distance)

    def eat(self, food):
        if not self.alive or not food.alive:
            return
        distance = math.sqrt((self.x - food.x) ** 2 + (self.y - food.y) ** 2)
        if distance < self.size and self.energy <= self.starvation_threshold:
            food.alive = False
            self.energy += random.randint(40, 80)

    def get_hitbox(self):
        return pygame.Rect(
            self.x - self.size, self.y - self.size,
            config.ORGANISM_HITBOX_RADIUS, config.ORGANISM_HITBOX_RADIUS)

    def render(self, screen):
        if self.alive:
            # Determine if the image should be flipped
            if self.x > self.previous_x:
                directed_avatar = pygame.transform.flip(self.avatar, True, False)
            else:
                directed_avatar = self.avatar

            # pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)  # circle as avatar
            screen.blit(directed_avatar, (self.x - self.size, self.y - self.size))
            font = pygame.font.SysFont(None, 24)
            text = font.render(f'{self.name} ({int(self.energy)})', True, (255, 255, 255))
            screen.blit(text, (self.x - self.size, self.y - self.size - 20))

    @staticmethod
    def random():
        x = random.randint(0, config.SCREEN_WIDTH)
        y = random.randint(0, config.SCREEN_HEIGHT)
        return Organism(x, y)
