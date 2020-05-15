import pygame


class StateManager:
    state_queue = []


class State:
    state_queue = StateManager.state_queue
    win = pygame.display.get_active()

    def __init__(self, *args, static_groups=None, mouse_interaction_groups=None, mouse=None, **kwargs):
        self.static_groups: list or None = static_groups
        self.mouse_interaction_groups: list or None = mouse_interaction_groups
        self.mouse = mouse
        self.state_queue.append(self)

        self.resume_state = {}

    def add_static_groups(self, *groups):
        for group in groups:
            self.static_groups.append(group)

    def remove_static_groups(self, *groups, do_kill=False):
        removed_groups =[]
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
                pass

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
                pass
        return removed_groups

    def exit(self, do_kill=True):
        self.state_queue.pop()
        if do_kill:
            del self
        else:
            return self

    def pause(self, *args, event_que=None, **kwargs):
        self.resume_state['mouse'] = self.mouse.state()
        self.resume_state['events'] = event_que

    def resume(self, *args, **kwargs):
        self.mouse
