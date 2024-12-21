import pygame
# from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK
import config
from organisms import Organism
from food import Food
from predators import Predator
from environment import Obstacle, Weather


def main():
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    organisms = [Organism.random() for _ in range(config.ORGANSIM_POPULATION)]
    predators = [Predator.random() for _ in range(config.PREDATOR_POPULATION)]
    obstacles = [Obstacle.random() for _ in range(config.NUMBER_OF_OBSTACLES)]
    food_items = [Food.random() for _ in range(config.ORGANSIM_FOOD)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill(config.BLACK)

        # Update organisms
        organisms = [o for o in organisms if o.alive]
        for organism in organisms:
            organism.move(food_items)
            for food in food_items:
                organism.eat(food)
            organism.render(screen)

        # Update predators
        predators = [p for p in predators if p.alive]
        for predator in predators:
            predator.move(organisms)
            predator.hunt(organisms)
            predator.render(screen)

        # Update obstacles
        for obstacle in obstacles:
            obstacle.render(screen)

        # Update food
        for food in food_items:
            food.render(screen)

        # Respawn food if needed
        if not any(food.alive for food in food_items):
            food_items = [Food.random() for _ in range(config.ORGANSIM_FOOD)]

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
