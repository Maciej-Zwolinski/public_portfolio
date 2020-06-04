from utility.singleton_pattern import Singleton
from utility.CustomExceptions import BreakException
from States import State, StateManager
from SpriteDerivedClasses import ClickableSprite
from mouse import Mouse

from settings import WIN_SIZE, FPS
import pygame


class Rectangle(pygame.sprite.Sprite):

    def __init__(self, size, colour, center, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface(size)
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.center = center


class Game(State, metaclass=Singleton):
    pass


class ExitButton(ClickableSprite):

    def __call__(self, *groups):
        return self.from_text("Exit", groups, center=(WIN_SIZE[0]//2, WIN_SIZE[1]//2))

    def on_lmb(self, mouse):
        StateManager.quit()


class ContinueButton(ClickableSprite):

    def __call__(self, *groups):
        return self.from_text("Continue", groups, center=(WIN_SIZE[0]//2, WIN_SIZE[1]//2 + 50))

    def on_lmb(self, mouse):
        pass


class MainMenu(State, metaclass=Singleton):

    def __init__(self, background=None):

        buttons = pygame.sprite.LayeredUpdates()
        ExitButton()(buttons)
        ContinueButton()(buttons)
        super().__init__(mouse_interaction_groups=[buttons],
                         background=background, mouse=Mouse(''))


if __name__ == '__main__':

    # startup
    pygame.init()
    run = True
    clock = pygame.time.Clock()

    win = pygame.display.set_mode(WIN_SIZE)
    pygame.display.set_caption("Game")

    # setting up screen
    mouse = Mouse('Player')
    # INTERACTABLES = pygame.sprite.LayeredUpdates()
    # exit_button = ExitButton()(INTERACTABLES)
    # exit_button = ExitButton.from_text("Exit", INTERACTABLES, center=(WIN_SIZE[0]//2, WIN_SIZE[1]//2))
    # menu = State(mouse_interaction_groups=[INTERACTABLES], mouse=mouse)

    menu = MainMenu()
    # starting game

    StateManager.loop(once=False)