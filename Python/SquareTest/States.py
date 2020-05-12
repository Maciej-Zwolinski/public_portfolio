import pygame

class State:
    state_queue = []

    def __init__(self, *args, **kwargs):
        self.state_queue.append(self)

    def exit(self):
        self.state_queue.pop()
        del self

    def pause(self):
        pass

    def resume(self):
        pass

    def loop(self, events=None):
        print(f'looping inside {0}'.format(self.__name__))
        self.exit()

class MainMenu(State):

