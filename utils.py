import random
import config
from organisms import Organism
from predators import Predator
from environment import Obstacle
from food import Food


def random_position():
    return random.randint(0, config.SCREEN_WIDTH), random.randint(0, config.SCREEN_HEIGHT)


def reset_simulation():
    organisms = [Organism.random() for _ in range(config.ORGANSIM_POPULATION)]
    predators = [Predator.random() for _ in range(config.PREDATOR_POPULATION)]
    obstacles = [Obstacle.random() for _ in range(config.NUMBER_OF_OBSTACLES)]
    food_items = [Food.random() for _ in range(config.ORGANSIM_FOOD)]
    return organisms, predators, obstacles, food_items
