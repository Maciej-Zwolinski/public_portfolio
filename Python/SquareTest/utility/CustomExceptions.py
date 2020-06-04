class BreakException(Exception):
    pass


class SwitchState(Exception):
    pass


class NoActiveState(Exception):

    def __str__(self):
        return 'State Queue empty, nothing to do here. Quitting.'
