import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK
from organisms import Organism
from food import Food
from predators import Predator
from environment import Obstacle, Weather


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Virtual Ecosystem")
    clock = pygame.time.Clock()

    # Initialize organisms, predators, food, and environment
    organisms = [Organism.random() for _ in range(4)]
    predators = [Predator.random() for _ in range(2)]
    food_items = [Food.random() for _ in range(50)]
    obstacles = [Obstacle.random() for _ in range(5)]
    weather = Weather()

    running = True
    weather_timer = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

        # Update weather
        weather_timer += 1
        if weather_timer >= weather.duration:
            weather = Weather()
            weather_timer = 0

        weather.apply_effects(organisms)
        weather.render(screen)

        # Update organisms
        new_organisms = []
        for i, organism in enumerate(organisms):
            organism.move()
            for food in food_items:
                organism.eat(food)
            for other in organisms[i+1:]:
                new_organisms.extend(organism.mate(other))
            organism.render(screen)

        organisms.extend(new_organisms)
        organisms = [o for o in organisms if o.alive]

        # Update predators
        for predator in predators:
            predator.move()
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
            food_items = [Food.random() for _ in range(50)]

        pygame.display.flip()
        clock.tick(1)

    pygame.quit()

if __name__ == "__main__":
    main()
