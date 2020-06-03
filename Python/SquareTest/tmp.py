from utility.singleton_pattern import Singleton
from States import State, StateManager
from SpriteDerivedClasses import ClickableSprite
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


class ExitButton(ClickableSprite):

    def __call__(self, *groups):
        return self.from_text(self.__class__, "Exit", groups, center=(WIN_SIZE[0]//2, WIN_SIZE[1]//2))

    def on_lmb(self, mouse):
        pygame.quit()

    def check(self):
        print("'it's me")


class Continue(ClickableSprite):
    def on_lmb(self, mouse):
        pass


class MainMenu(State, metaclass=Singleton):

    def __init__(self, background=None):
        background = pygame.sprite.Sprite() if background is None else background
        # exit_button =
        # outside_box = Rectangle()

        super().__init__(static_groups=[pygame.sprite.Group()],
                         mouse_interaction_groups=[pygame.sprite.LayeredUpdates()],
                         mouse=Mouse(''))


if __name__ == '__main__':

    def draw_window(win, sprites):
        win.fill((255, 255, 255))
        sprites.draw(win)
        pygame.display.update()

    # startup
    pygame.init()
    run = True
    clock = pygame.time.Clock()

    win = pygame.display.set_mode(WIN_SIZE)
    pygame.display.set_caption("Game")

    # setting up screen
    mouse = Mouse('Player')
    INTERACTABLES = pygame.sprite.LayeredUpdates()
    exit_button = ExitButton(INTERACTABLES)
    menu = State(mouse_interaction_groups=[INTERACTABLES])


    # starting game

    while run:
        print('------')
        clock.tick(FPS)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()

        mouse.update(events)

        draw_window(win, INTERACTABLES)
