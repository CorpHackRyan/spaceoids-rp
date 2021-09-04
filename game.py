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
        self.asteroid = Asteroid((400, 300))

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

    def _process_game_logic(self):
        self.spaceship.move()
        #self.asteroid.move()

        pass

    def _draw(self):
        # draw a blue screen ->  self.screen.fill((0, 0, 255))

        #.blit This method takes two arguments:
        # 1- The surface that you want to draw
        # 2- The point where you want to draw it
        # x and y coordinates start at the top left corner of the window
        self.screen.blit(self.background, (0, 0))
        self.spaceship.draw(self.screen)
        #self.asteroid.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(self.frames_per_second)
