import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT


def random_position():
    return random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)
