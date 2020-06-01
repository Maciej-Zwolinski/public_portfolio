from States import State, StateManager
from SpriteDerivedClasses import Button
from .utility.singleton_pattern import Singleton
from mouse import Mouse

from settings import WIN_SIZE, FPS
import pygame


class Game(State, metaclass=Singleton):
    pass


class Rectangle(pygame.sprite.Sprite):

    def __init__(self, size, colour, center, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface(size)
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.center = center


class ExitButton(Button):

    def __init__(self):
        super().from_text("Exit")

    def on_lmb(self, mouse):
         StateManager.quit()

class Continue(Button):
    def on_lmb(self, mouse):




class MainMenu(State, metaclass=Singleton):

    def __init__(self, background=None):
        background = pygame.sprite.Sprite() if background is None else background
        exit_button =
        outside_box = Rectangle()

        super().__init__(static_groups=[pygame.sprite.Group()],
                         mouse_interaction_groups=[pygame.sprite.LayeredUpdates()],
                         mouse=Mouse(''))

