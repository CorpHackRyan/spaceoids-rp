from pygame.image import load
from pygame.math import Vector2
import random


def load_sprite(name, with_alpha=True):
    path = f"assets/sprites/{name}.png"
    loaded_sprite = load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()

    else:
        return loaded_sprite.convert()

def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)


def get_random_position(surface):
    # This will generate a random set of coordinates on a given surface and return the result as a Vector2 instance.
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height()),
    )

