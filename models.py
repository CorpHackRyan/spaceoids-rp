from pygame.math import Vector2
from utils import load_sprite
from pygame.transform import rotozoom     # responsible for scaling and rotating images:

# Remember that Pygame’s y-axis goes from top to bottom, so a negative value actually points upwards:
const_UP = Vector2(0, -1)


class GameObject:
    def __init__(self, position, sprite, velocity):
        # ensure that the position and the velocity will always be represented as vectors for future calculations,
        # even if tuples are passed to the constructor. You do that by calling the Vector2() constructor.
        self.position = Vector2(position)          # The center of the object
        self.sprite = sprite                       # the image used to draw this object

        # calculates the radius as half the width of the sprite image. In this program, game object sprites will
        # always be squares with transparent backgrounds. You could also use the height of the image—it would make
        # no difference.
        self.radius = sprite.get_width() / 2

        self.velocity = Vector2(velocity)          # Updates the position of the object each frame

    def draw(self, surface):
        angle = self.direction.angle_to(const_UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())

        # draw the objects sprite on the surface passed as an argument
        blit_position = self.position - rotated_surface_size * 0.5

        surface.blit(rotated_surface, blit_position)


    def move(self):
        #  It will update the position of the game object.
        self.position = self.position + self.velocity

    def collides_width(self, other_obj):
        # calculate distance between 2 objects using distance_to function.
        # checks if that distance is smaller than the sum of the objects’ radiuses. If so, the objects collide.
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius


class Spaceship(GameObject):
    # DIRECTION is a vector describing where the spaceship is pointing.
    # VELOCITY is a vector describing where the spaceship moves each frame.
    # ACCELERATION is a constant number describing how fast the spaceship can speed up each frame.


    # this value represents an angle in degrees by which your spaceship’s direction can rotate each frame.
    const_MANEUVERABILITY = 3

    def __init__(self, position):
        # Make a copy of the original UP vector set as a const in the spaceship class
        self.direction = Vector2(const_UP)

        # This calls the GameObject constructor with a specific image and zero velocity
        super().__init__(position, load_sprite("spaceship"), Vector2(0, 0))

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.const_MANEUVERABILITY * sign

        # rotates it in place by a given angle in degrees. - from vector2 class
        self.direction.rotate_ip(angle)


class Asteroid(GameObject):
    def __init__(self, position):
        super().__init__(position, load_sprite("asteroid"), Vector2(1, 0))

