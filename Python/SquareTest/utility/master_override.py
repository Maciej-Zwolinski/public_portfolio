from functools import wraps


def master_override(masters=None):
    """
    :param masters:
        has to be iterable
        [1] if None is provided, then it is asserted that object has an attribute called 'masters' or 'master'
            this supports single object as a master, by wrapping it into a list
    :return:
        [2] Resulting iterable is then searched for any object that has a method called 'func', then calls it
        [3] if none are found, the function is called without modification
    """
    def wrapper(func):
        @wraps(func)
        def method_wrapper(self, *args, **kwargs):
            if masters is None:  # [1]
                try:
                    _masters = getattr(self, 'masters')
                except AttributeError:
                    try:
                        _masters = [getattr(self, 'master')]
                    except AttributeError:
                        raise AttributeError("'None' type argument was passed to the 'master_override' function and\
                         'masters' and 'master' attributes lookup failed for {0}".format(self.__name__))
            else:
                _masters = masters
            for master in _masters:  # [2]
                if hasattr(master, func.__name__):
                    return getattr(master, func.__name__)(self, *args, **kwargs)
            return func(self, *args, **kwargs)  # [3]
        return method_wrapper
    return wrapper


if __name__ == '__main__':

    class Master:

        def __init__(self, name):
            self.name = name


    class Devil(Master):

        def __init__(self):
            super().__init__("Devil")

        def work(self, slave):
            print("{0}, I'm the Devil and you will obey me. You work for me now!".format(slave.name))
            print("-------------")

        def drink(self, slave):
            print("{0}, I'm the Devil and you will obey me. You will drink what I tell you to!".format(slave.name))
            print("-------------")


    class God(Master):

        def __init__(self):
            super().__init__("God")

        def work(self, slave):
            print("{0}, I'm God and you will obey me. You work for me now!".format(slave.name))
            print("-------------")

        def eat(self, slave):
            print("{0}, I'm God and you will obey me. You will eat what I tell you to!".format(slave.name))
            print("-------------")


    class Slave:

        def __init__(self, name, *masters):
            self.name = name
            self.masters = [*masters]

        @master_override()
        def work(self):
            print("I'm {} and I do what I want!".format(self.name))
            print("-------------")

        @master_override()
        def rest(self):
            print("I'm {} and I rest when I want!".format(self.name))
            print("-------------")

        @master_override()
        def drink(self):
            print("I'm {} and I drink what I want!".format(self.name))
            print("-------------")

        @master_override()
        def eat(self):
            print("I'm {} and I eat what I want!".format(self.name))
            print("-------------")


    hiob = Slave("Hiob", God(), Devil())

    hiob.work()
    hiob.eat()
    hiob.drink()
    hiob.rest()
