import pygame
from States import StateManager, State
from mouse import Mouse
from SpriteDerivedClasses import MouseIntractableSprite

INTERFACE_LAYER = 100
WIN_SIZE = (1600, 900)
FPS = 1

INTERACTABLES = MouseIntractableSprite.mouse_interaction_group
HIGHLIGHTED_SPRITES = MouseIntractableSprite.highlighted_sprites


def draw_window(win, sprites):
    win.fill((255, 255, 255))
    sprites.draw(win)
    pygame.display.update()


class SmallSquare(MouseIntractableSprite):

    def __init__(self, colour, center, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((100,100))
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self._anchor_point = center

    def on_lmb(self, mouse):
        print('I got clicked with Left Button')

    def on_rmb(self, mouse):
        print('I got clicked with Right Button')


def main():
    # startup
    pygame.init()
    run = True
    clock = pygame.time.Clock()

    win = pygame.display.set_mode(WIN_SIZE)
    pygame.display.set_caption("Client")

    # setting up screen
    mouse = Mouse('Player')
    box = SmallSquare((128, 0, 0), (800, 450))
    # starting game

    if INTERACTABLES:
        print('sprites initialized')
    print("starting game")

    while run:
        print('------')
        clock.tick(FPS)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return 1

        mouse.update(events)
        box.update()

        draw_window(win, INTERACTABLES)


main()
