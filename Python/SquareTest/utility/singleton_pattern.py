from weakref import WeakValueDictionary


class Singleton(type):
    _instances = WeakValueDictionary()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super(Singleton, cls).__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


if __name__ == '__main__':

    class Boss(metaclass=Singleton):

        def __init__(self, name):
            self.name = name

        def __str__(self):
            return self.name

    print('naming Boss Joe')
    x = Boss('Joe')
    print(f'Boss.name is {x}')
    print('trying to rename the Boss to Cindy')
    y = Boss('Cindy')
    print(f'Boss.name is {y}')

    del x, y
    print(Boss('Cindy'))
