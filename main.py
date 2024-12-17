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
    pygame.display.set_caption("Virtual Ecosystem")
    clock = pygame.time.Clock()

    # Initialize organisms, predators, food, and environment
    organisms = [Organism.random() for _ in range(config.ORGANSIM_POPULATION)]
    predators = [Predator.random() for _ in range(config.PREDATOR_POPULATION)]
    food_items = [Food.random() for _ in range(config.ORGANSIM_FOOD)]
    obstacles = [Obstacle.random() for _ in range(5)]
    weather = Weather()

    running = True
    weather_timer = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(config.BLACK)

        # Update weather
        weather_timer += 1
        if weather_timer >= weather.duration:
            weather = Weather()
            weather_timer = 0

        weather.apply_effects(organisms)
        weather.render(screen)

        # Update organisms
        # new_organisms = []
        # for i, organism in enumerate(organisms):
        #     organism.move()
        #     for food in food_items:
        #         organism.eat(food)
        #     for other in organisms[i + 1:]:
        #         new_organisms.extend(organism.mate(other))
        #     organism.render(screen)

        # organisms.extend(new_organisms)
        # organisms = [o for o in organisms if o.alive]
        for organism in organisms:
            organism.move(food_items)
            for food in food_items:
                organism.eat(food)
            organism.render(screen)

        # Update predators
        # for predator in predators:
        #     predator.move()
        #     predator.hunt(organisms)
        #     predator.render(screen)
        for predator in predators:
            predator.move(organisms)
            predator.hunt(organisms)
            predator.render(screen)

        predators = [p for p in predators if p.alive]

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
