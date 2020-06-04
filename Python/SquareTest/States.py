import pygame
from utility.object_save_load import save_object_internal_state_to_dict, load_object_internal_state_from_dict
from utility.singleton_pattern import Singleton
from utility.classproperty import class_property
from utility.CustomExceptions import *

from settings import FPS


class StateManager(metaclass=Singleton):

    state_queue = []

    @class_property
    def active_state(cls):
        try:
            return cls.state_queue[-1]
        except (AttributeError, IndexError):
            raise NoActiveState

    @classmethod
    def quit(cls):
        for state in reversed(cls.state_queue):
            state.exit()
        pygame.quit()

    @classmethod
    def loop(cls, once=True):
        while True:
            try:
                pygame.time.Clock().tick(FPS)
                print('-----')
                cls.active_state.update()
                cls.active_state.draw()
            except NoActiveState as e:
                print(e)
                break
            if once:
                break


class State:
    state_queue = StateManager.state_queue

    def __init__(self, *args, static_groups=None, mouse_interaction_groups=None, background=None, mouse=None, **kwargs):
        self.static_groups: list or None = [] if static_groups is None else static_groups
        self.mouse_interaction_groups: list or None = \
            [] if mouse_interaction_groups is None else mouse_interaction_groups
        self.background = background
        self.mouse = mouse
        self.state_queue.append(self)

        self.resume_state = {}

    @property
    def win(self):
        return pygame.display.get_surface()

    def add_static_groups(self, *groups):
        for group in groups:
            self.static_groups.append(group)

    def remove_static_groups(self, *groups, do_kill=False):
        removed_groups = []
        for group in groups:
            try:
                self.static_groups.remove(group)
                if do_kill:
                    for sprite in group.sprites():
                        del sprite
                    del group
                else:
                    removed_groups.append(group)
            except ValueError:
                continue

    def add_mouse_interaction_groups(self, *groups):
        for group in groups:
            self.mouse_interaction_groups.append(group)

    def remove_mouse_interaction_groups(self, *groups, do_kill=False):
        removed_groups = []
        for group in groups:
            try:
                self.mouse_interaction_groups.remove(group)
                if do_kill:
                    for sprite in group.sprites():
                        del sprite
                    del group
                else:
                    removed_groups.append(group)
            except ValueError:
                continue
        return removed_groups

    def exit(self, do_kill=True):
        self.state_queue.pop()
        if do_kill:
            if self.static_groups:
                self.remove_static_groups((*self.static_groups,), do_kill=True)
            if self.mouse_interaction_groups:
                self.remove_mouse_interaction_groups((*self.mouse_interaction_groups,), do_kill=True)
            del self
            return None
        else:
            return self

    def pause(self, *args, event_que=None, clear_event_queue=False, **kwargs):
        mouse_state_keys = ('pos', 'active_object', 'drag_mode', {'_lmb': ('primed', 'primed_position')},
                            {'_rmb': ('primed', 'primed_position')})
        self.resume_state['mouse'] = save_object_internal_state_to_dict(self.mouse, mouse_state_keys)
        if clear_event_queue:
            self.resume_state['event_queue'] = event_que
            pygame.event.clear()
        else:
            self.resume_state['event_queue'] = []
        return self.win.copy(), self.mouse

    def resume(self, *args, clear=True, **kwargs):
        # load mouse object
        load_object_internal_state_from_dict(self.mouse, self.resume_state['mouse'])
        if clear:
            # clears event queue upon resuming
            pygame.event.clear()
        # reload state queue
        for event in self.resume_state['event_queue']:
            pygame.event.post(event)
        # update the mouse position and resolve any remaining events
        self.mouse.update()
        self.resume_state = {}

    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                StateManager.quit()
        self.mouse.update(events)

    def draw(self):
        if self.background:
            self.win.blit(self.background)
        else:
            self.win.fill((255, 255, 255))
        for static_group in self.static_groups:
            static_group.draw(self.win)
        for instractive_group in self.mouse_interaction_groups:
            instractive_group.draw(self.win)
        pygame.display.flip()
