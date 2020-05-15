from utility_funtions import save_object_internal_state_to_dict, load_object_internal_state_from_dict


class Obj2:
    def __init__(self, z):
        self.z = z

    def default_save(self):
        return save_object_internal_state_to_dict(self, 'z')

    def load_internal_state(self, _dictionary):
        load_object_internal_state_from_dict(self, _dictionary)

    def __str__(self):
        return 'Obj2: ' + str(self.z) + ', '


class Obj3:
    def __init__(self, x, y):
        self.x, self.y = x, Obj2(y)

    def default_save(self):
        return save_object_internal_state_to_dict(self, 'x', {'y': ()})

    def load_internal_state(self, _dictionary):
        load_object_internal_state_from_dict(self, _dictionary)

    def __str__(self):
        return 'Obj3: ' + str(self.x) + ' ' + str(self.y)+', '


class Obj1:
    def __init__(self, attr1, x, y, z):
        self.attr1 = attr1
        self.attr2 = Obj2(z)
        self.attr3 = Obj3(x, y)

    def default_save(self):
        return save_object_internal_state_to_dict(self, 'attr1')

    def __str__(self):
        return 'Obj1: ' + str(self.attr1) + '  ' + str(self.attr2) + ' ' + str(self.attr3)


obj = Obj1(3, 1, 2, 7)
dictionary = save_object_internal_state_to_dict(obj, (), {'attr2': ()}, {'attr3': ()})
print(dictionary)
print(obj)
print("small change")
obj = Obj1(4, 2, 3, 8)
print(obj)
print('trying to revert changes...')
load_object_internal_state_from_dict(obj, dictionary)
print(obj)



