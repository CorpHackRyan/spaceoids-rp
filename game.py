import pygame
import sys
from utils import load_sprite, get_random_position
from models import Spaceship, Asteroid


class SpaceRocks:
    # constant representing an area that has to remain empty. 250 pixels should be enough:
    const_MIN_ASTEROID_DISTANCE = 250

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)

        # game to run with a fixed number of frames per second (FPS).
        self.clock = pygame.time.Clock()

        # This method will wait long enough to match the desired FPS value,# passed as an argument.
        self.frames_per_second = 60

        # Old way, generated the asteroids, but overlapped the space ship.
        # self.asteroids = [
        #    Asteroid(get_random_position(self.screen)) for _ in range(6)]
        self.asteroids = []
        self.bullets = []

        # Now add the callback to the spaceship when it’s created. Bullets are stored as a list, and the only
        # thing the callback has to do is add new items to that list. Therefore, the append()
        # method should do the job.
        self.spaceship = Spaceship((400, 300), self.bullets.append)

        # Below will ensure that no asteroid is touching the space ship when you start

        for _ in range(6):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.const_MIN_ASTEROID_DISTANCE
                ):
                    break

                self.asteroids.append(Asteroid(position))

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Spaceoids")

    def _handle_input(self):
        for event in pygame.event.get():
            print(event)

            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
                sys.exit()
            elif (
                # input handling. The bullet should be generated only when Space pressed, so you can use
                # the event loop. The constant for Space is pygame.K_SPACE.

                self.spaceship
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
            ):
                self.spaceship.shoot()

            is_key_pressed = pygame.key.get_pressed()

            if self.spaceship:
                if is_key_pressed[pygame.K_RIGHT]:
                    self.spaceship.rotate(clockwise=True)
                elif is_key_pressed[pygame.K_LEFT]:
                    self.spaceship.rotate(clockwise=False)
                if is_key_pressed[pygame.K_UP]:
                    self.spaceship.accelerate()

    def _process_game_logic(self):
        #below was the old way to move the spaceship and asteroids
        #self.spaceship.move(self.screen)
        #self.asteroid.move()

        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_width(self.spaceship):
                    self.spaceship = None
                    break

    def _draw(self):
        # draw a blue screen ->  self.screen.fill((0, 0, 255))

        #.blit This method takes two arguments:
        # 1- The surface that you want to draw
        # 2- The point where you want to draw it
        # x and y coordinates start at the top left corner of the window
        self.screen.blit(self.background, (0, 0))

        # Old to draw single items on the screen, now we will do it with multiple objects in a loop
        # self.spaceship.draw(self.screen)
        # self.asteroid.draw(self.screen)

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(self.frames_per_second)

    def _get_game_objects(self):
        # OLD WAY : return [*self.asteroids, self.spaceship]
        game_objects = [*self.asteroids, *self.bullets]

        # Now that it’s possible for the spaceship to have a value of None, it’s important to update
        # _get_game_objects() in the SpaceRocks class to avoid trying to render or move a destroyed
        # spaceship:

        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects

