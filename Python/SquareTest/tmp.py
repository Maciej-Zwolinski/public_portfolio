from utility.singleton_pattern import Singleton
from utility.CustomExceptions import BreakException
from States import State, StateManager
from SpriteDerivedClasses import ClickableSprite
from mouse import Mouse

from settings import WIN_SIZE, FPS
import pygame
SCREEN_CENTER = (WIN_SIZE[0]//2, WIN_SIZE[1]//2)


class Rectangle(pygame.sprite.Sprite):

    def __init__(self, *groups, size=(0, 0), colour=(0, 0, 0), image=None, center=None, topleft=None):
        super().__init__(*groups)
        if not image:
            self.image = pygame.Surface(size)
            self.image.fill(colour)
        else:
            self.image = image
        self.rect = self.image.get_rect()
        if center:
            self.rect.center = center
        elif topleft:
            self.rect.topleft = topleft
        else :
            self.rect.topleft = (0, 0)


class Game(State, metaclass=Singleton):
    pass


class MainMenu(State):

    def __init__(self, background=None):

        buttons = pygame.sprite.LayeredUpdates()
        outline = pygame.sprite.Group()

        self.MainBox(outline)
        self.ExitButton()(buttons)
        self.ContinueButton()(buttons)
        super().__init__(static_groups=[outline], mouse_interaction_groups=[buttons],
                         background=background, mouse=Mouse(''))

    class ContinueButton(ClickableSprite):

        def __call__(self, *groups):
            return self.from_text("Continue", groups, center=(WIN_SIZE[0] // 2, WIN_SIZE[1] // 2 + 35))

        def on_lmb(self, mouse):
            StateManager.active_state.exit()

    class ExitButton(ClickableSprite):

        def __call__(self, *groups):
            return self.from_text("Exit", groups, center=SCREEN_CENTER)

        def on_lmb(self, mouse):
            StateManager.quit()

    class MainBox(Rectangle):

        def __init__(self, *groups):
            super().__init__(*groups, size=(400, 150), colour=(64, 64, 64), center=SCREEN_CENTER)
            font = pygame.font.Font('freesansbold.ttf', 50)
            text_render = font.render("Main Menu", True, (255, 255, 255), (0, 0, 0))
            self.image.blit(source=text_render, dest=((self.image.get_width()-text_render.get_width())//2, 0))


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

    background = pygame.Surface(WIN_SIZE)
    background.fill((64, 64, 64))
    MainMenu(background=background)
    MainMenu()
    # starting game

    StateManager.loop(once=False)
