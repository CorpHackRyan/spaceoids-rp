import pygame
import sys
from utils import load_sprite
from models import Spaceship, Asteroid


class SpaceRocks:
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)

        # game to run with a fixed number of frames per second (FPS).
        self.clock = pygame.time.Clock()

        # This method will wait long enough to match the desired FPS value,# passed as an argument.
        self.frames_per_second = 60

        self.spaceship = Spaceship((400, 300))
        self.asteroids = [
            Asteroid((0, 0)) for _ in range(6)]

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

            is_key_pressed = pygame.key.get_pressed()

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
        return [*self.asteroids, self.spaceship]
