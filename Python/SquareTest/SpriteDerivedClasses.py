import pygame


class ClickableSprite(pygame.sprite.Sprite):

    def __init__(self, *groups, image=None, center=None, topleft=None, **kwargs):
        """
        :param groups: groups to which currently created sprite is supposed to be attached to
        :param image: initial image to build the button from
        :param center: position of the center of the button, ignored if image not given
        :param topleft: position of the topleft of the button, ignored if image not given

        if image and center not given, than virtual sprite is created
        if image given, than center or topleft dictates where the button should appear
        """
        super().__init__(groups)
        self.image: pygame.Surface or None = image
        self.rect: pygame.Rect or None = self.image.get_rect() if self.image else None
        if self.image and center:
            self.rect.center = center
        elif self.image and topleft:
            self.rect.topleft = topleft

    @classmethod
    def from_text(cls, text, *groups, center=None, topleft=None, text_size=32, font_name='freesansbold.ttf',
                  text_colour=(128, 0, 0), background_colour=(0, 0, 0)):
        font = pygame.font.Font(font_name, text_size)
        text_render = font.render(text, True, text_colour, background_colour)
        button = cls(groups, image=text_render, center=center, topleft=topleft)
        return button

    def on_lmb(self, mouse):
        """placeholder function used to control interaction with LeftMouseButton"""
        print("placeholder 'on_lmb' function called")
        pass

    def on_rmb(self, mouse):
        """placeholder function used to control interaction with RightMouseButton"""
        print("placeholder 'on_rmb' function called")
        pass


class MouseIntractableSprite(ClickableSprite):
    """Class expands basic sprite class, providing extra functionality for clicking and dragging"""

    mouse_interaction_group = pygame.sprite.LayeredUpdates()
    highlighted_sprites = []

    def __init__(self, *groups, **kwargs):
        """
        _layer: attribute needed work with LayerdUpdates group
        _anchor_point: last semi-permanent position, used to save the return point in case anything goes wrong
        """
        super().__init__(*groups, **kwargs)

        self._anchor_point = self.rect.center if self.rect else None

        self._layer = 0
        self.mouse_interaction_group.add(self)

    @property
    def layer(self):
        return self._layer

    @layer.setter
    def layer(self, new_layer):
        if new_layer < 0:
            self._layer = 0
        else:
            self._layer = new_layer

    @property
    def anchor_point(self):
        return self._anchor_point

    def __set_anchor_point(self):
        self._anchor_point = self.rect.center

    def return_to_anchor_point(self):
        self.rect.center = self._anchor_point

    def drop(self):
        """wrapper method for __set_anchor_point, allows to set new permanent location for the object"""
        self.__set_anchor_point()

    def highlight(self):
        """placeholder method controlling highlight behaviour"""
        self.highlighted_sprites.append(self)

    def drag(self, dx_dy):
        """moves the sprite by (dx, dy)"""
        x, y = self._anchor_point
        dx, dy = dx_dy
        self.rect.center = (x+dx, y+dy)