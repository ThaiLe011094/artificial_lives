import pygame
# from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK
import config
from organisms import Organism
from food import Food
from predators import Predator
from environment import Obstacle, Weather
from utils import reset_simulation


def main():
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Reset or init
    organisms, predators, obstacles, food_items = reset_simulation()

    dragging = False
    selected_entity = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    organisms, predators, obstacles, food_items = reset_simulation()
                elif event.key == pygame.K_q:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    for organism in organisms:
                        if organism.get_hitbox().collidepoint(event.pos):
                            dragging = True
                            selected_entity = organism
                            break
                    if not dragging:
                        for predator in predators:
                            if predator.get_hitbox().collidepoint(event.pos):
                                dragging = True
                                selected_entity = predator
                                break
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    dragging = False
                    selected_entity = None
            elif event.type == pygame.MOUSEMOTION:
                if dragging and selected_entity:
                    selected_entity.x, selected_entity.y = event.pos

        # Clear the screen
        screen.fill(config.BACKGROUND_COLOR)

        # Update organisms
        organisms = [o for o in organisms if o.alive]
        for organism in organisms:
            if not dragging or organism != selected_entity:
                organism.move(food_items, predators)
            for food in food_items:
                organism.eat(food)
            organism.render(screen)

        # Update predators
        predators = [p for p in predators if p.alive]
        for predator in predators:
            if not dragging or predator != selected_entity:
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
