from pygame.math import Vector2
from utils import get_random_velocity, load_sprite, wrap_position
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

    def move(self, surface):
        #  It will update the position of the game object.
        # self.position = self.position + self.velocity     - old way of doing the position movement,

        # New way is to use the new function wrap_position so we wrap around the screen
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_width(self, other_obj):
        # calculate distance between 2 objects using distance_to function.
        # checks if that distance is smaller than the sum of the objects’ radii. If so, the objects collide.
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius


class Spaceship(GameObject):
    # DIRECTION is a vector describing where the spaceship is pointing.
    # VELOCITY is a vector describing where the spaceship moves each frame.
    # ACCELERATION is a constant number describing how fast the spaceship can speed up each frame.

    # this value represents an angle in degrees by which your spaceship’s direction can rotate each frame.
    const_MANEUVERABILITY = 30
    const_ACCELERATION = 0.25
    const_BULLET_SPEED = 3

    # Adding CREATE BULLET CALLBACK to the __init__ function of the SpaceShip class and why
    #
    # There’s a small issue with shooting. Bullets are stored in the main game object, represented by the
    # SpaceRocks class. However, the shooting logic should be determined by the spaceship. It’s the
    # spaceship that knows how to create a new bullet, but it’s the game that stores and later animates
    # the bullets. The Spaceship class needs a way to inform the SpaceRocks class that a bullet has been
    # created and should be tracked.
    #
    # To fix this, you can add a callback function to the Spaceship class. That function will be
    # provided by the SpaceRocks class when the spaceship is initialized. Every time the spaceship
    # creates a bullet, it will initialize a Bullet object and then call the callback. The callback
    # will add the bullet to the list of all bullets stored by the game.
    # Start by adding a callback to the constructor of the Spaceship class

    def __init__(self, position, create_bullet_callback):
        self.create_bullet_callback = create_bullet_callback
        # Make a copy of the original UP vector set as a const in the spaceship class
        self.direction = Vector2(const_UP)

        # This calls the GameObject constructor with a specific image and zero velocity
        super().__init__(position, load_sprite("spaceship"), Vector2(0))

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.const_MANEUVERABILITY * sign

        # rotates it in place by a given angle in degrees. - from vector2 class
        self.direction.rotate_ip(angle)

    def accelerate(self):
        self.velocity += self.direction * self.const_ACCELERATION

    def shoot(self):
        # You start by calculating the velocity of the bullet. The bullet is always shot forward, so you use
        # the direction of the spaceship multiplied by the speed of the bullet. Because the spaceship doesn’t
        # necessarily stand still, you add its velocity to the velocity of the bullet. That way, you can create
        # high-speed bullets if the spaceship is moving very fast.
        #
        # Then you create an instance of the Bullet class at the same location as the spaceship, using
        # the velocity that was just calculated. Finally, the bullet is added to all the bullets in the game
        # by using the callback method.

        bullet_velocity = self.direction * self.const_BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)


class Asteroid(GameObject):
    def __init__(self, position):
        self.direction = Vector2(const_UP)

        # Old way before randomly assigning velocity to asteroids
        # super().__init__(position, load_sprite("asteroid"), Vector2(0, 0))
        super().__init__(position, load_sprite("asteroid"), get_random_velocity(1, 3))


class Bullet(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("bullet"), velocity)
        self.direction = Vector2(const_UP)
