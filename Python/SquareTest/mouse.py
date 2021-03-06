import pygame
from SpriteDerivedClasses import MouseIntractableSprite

from utility_funtions import abs_distance, distance_xy

DRAG_ENGAGE_MIN_SHIFT = 25


class Mouse(pygame.sprite.Sprite):
    """
    Mouse class controls all interactions between sprites and pygame.mouse object.
    """

    handled_events = [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]
    # sprites that the mouse can interact with
    mouse_interaction_group = MouseIntractableSprite.mouse_interaction_group

    def __init__(self, owner, *groups, initial_position=None):
        """
        :param owner: entity that controls the mouse (player)
        image, rect: placeholder objects that will be used to support interactions with sprite groups that
                    do not support point collisions
        pos: current mouse position (int, int)
        drag_mode: controls interaction between mouse movements and object interacted with
        active_object: object with which mouse interacts
        """
        super().__init__(*groups)
        self.image = pygame.Surface([1, 1])
        self.rect = self.image.get_rect()
        self.pos = None
        self.owner = owner
        self.lmb = Mouse.LeftMouseButton(self)
        self.rmb = Mouse.RightMouseButton(self)
        self.drag_mode = False
        self.active_object: MouseIntractableSprite or None = None
        self.update(set_pos=initial_position) if initial_position else self.update()

    def drop_active_object(self):
        self.lmb.clear()
        self.rmb.clear()
        if self.drag_mode:
            self.drag_mode = False
        if self.active_object:
            self.active_object.drop()
            self.active_object = None

    def abandon_active_object(self):
        """return active object to its last permanent location"""
        self.lmb.clear()
        self.rmb.clear()
        if self.drag_mode:
            self.drag_mode = False
        if self.active_object:
            self.active_object.return_to_anchor_point()
            self.active_object = None

    class MouseButton:
        """
        class that holds mouse button states, detects object collisions and handles clicks
        """

        def __init__(self, mouse):
            self.mouse: Mouse = mouse
            self.primed = False
            self.primed_position = None

        def prime(self, position):
            """
            :param position: where priming occurred

            detects collision with topmost interactable sprite, if none are detected ignores input
            """
            try:
                self.mouse.active_object = self.mouse.mouse_interaction_group.get_sprites_at(position)[-1]
                self.primed = True
                self.primed_position = position
            except IndexError:
                pass

        def release(self):
            """Placeholder function to control button release"""
            pass

        def clear(self):
            """Offers a way to clear button state"""
            self.primed = False
            self.primed_position = None

    # TODO: think of another way of binding keys without creating subclasses
    class LeftMouseButton(MouseButton):

        def release(self):
            if self.primed:
                self.mouse.active_object.on_lmb(self.mouse)
                self.mouse.active_object = None
                self.clear()

    class RightMouseButton(MouseButton):

        def release(self):
            if self.primed:
                self.mouse.active_object.on_rmb(self.mouse)
                self.mouse.active_object = None
                self.clear()

    def update(self, event_list=None, set_pos=None, move=None, **kwargs):
        # TODO: get rid of the **kwargs as they aren't strictly necessary
        """
        :param event_list:
        expects no arguments to update position or list of pygame.event to interact with
        event_handle class variable is used to initially filter the list of events passed
        :param set_pos:
            set_pos = (x,y) -- moves the cursor to chosen position
        :param move:
            move = (dx, dy) -- moves the cursor by (dx, dy)
        """

        if event_list is None:
            event_list = []
        if set_pos:
            x, y = set_pos
            pygame.mouse.set_pos(x, y)
        if move:
            dx, dy = move
            x, y = self.pos
            pygame.mouse.set_pos(x + dx, y + dy)

        self.pos = pygame.mouse.get_pos()

        """
        handling of passed events (if any)
        first the events are filtered, then they are evaluated one by one described by following logic tree:

        if the mouse is currently dragging an object and returns near the original location: 
            the dragging will be cancelled and the dragged object will return to it's original location
        if the mouse is currently dragging:
            if rmb was pressed:
                dragging will be canceled and the dragged object will return to it's original location
                buttons will reset
            if lmb was released:
                dragged object will be dropped off at the event location
        else:
            if button 'x' was primed and 'x' is being released:
                active_object will receive appropriate click command
            if button 'x' was primed and 'y' is being primed:
                #: this is not properly implemented!!!
                button 'x' will be reset
                button 'y' will be primed 
        """
        if event_list:
            # filter events
            events = filter(lambda event: event.type in self.handled_events, event_list)

            # dragging is initiated by left mouse button only and disabled by right clicks
            for event in events:
                # if the mouse in a drag mode, but we returned to nearby location, we want to cancel dragging
                if self.drag_mode and abs_distance(event.pos, self.lmb.primed_position) < DRAG_ENGAGE_MIN_SHIFT:
                    self.active_object.return_to_anchor_point()
                    self.drag_mode = False

                if self.drag_mode and self.active_object:
                    # lmb released:
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        self.active_object.drag(distance_xy(self.lmb.primed_position, event.pos))
                        self.drop_active_object()
                        continue
                    # rmb pressed:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                        self.abandon_active_object()
                        continue

                elif not self.drag_mode:
                    if self.lmb.primed:
                        if event.button == 1 and event.type == pygame.MOUSEBUTTONUP:
                            self.lmb.release()
                            continue
                    else:
                        if event.button == 1 and event.type == pygame.MOUSEBUTTONDOWN:
                            self.lmb.prime(event.pos)
                            continue

                    if self.rmb.primed:
                        if event.button == 3 and event.type == pygame.MOUSEBUTTONUP:
                            self.rmb.release()
                            continue
                    else:
                        if event.button == 3 and event.type == pygame.MOUSEBUTTONDOWN:
                            self.rmb.prime(event.pos)
                            continue
        """
        finally, if we have an active_object:
            if left button is primed and we moved sufficiently far away:
                engage dragging mode 
            if the mouse is in dragging mode:
                if the mouse returned sufficiently close to original location:
                    cancel dragging and return object to it's original position
                else:
                    we want to drag active_object to mouse current location

        """
        if self.active_object:
            from_, to_ = (self.lmb.primed_position, self.pos)
            if not self.drag_mode:
                if self.lmb.primed and abs_distance(from_, to_) >= DRAG_ENGAGE_MIN_SHIFT:
                    self.drag_mode = True
                    self.active_object.drag(distance_xy(from_, to_))
            else:
                if abs_distance(from_, to_) < DRAG_ENGAGE_MIN_SHIFT:
                    self.active_object.return_to_anchor_point()
                else:
                    self.active_object.drag(distance_xy(from_, to_))

        self.rect.center = self.pos
