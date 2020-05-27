
def load_object_internal_state_from_dict(obj, dictionary):
    """
    this function is not supposed to be used to initialize objects
    if a key represents simple variable then it's value is directly loaded
    if en existing attribute is a dict, then the value is copied without unpacking
    an attempt is made to further unpack dictionary, if it fails, it is assumed the dictionary has been unpacked fully
    """
    for key in dictionary.keys():
        if hasattr(obj, key):
            if isinstance(getattr(obj, key), dict):
                setattr(obj, key, dictionary.get(key))
            else:
                try:
                    load_object_internal_state_from_dict(getattr(obj, key), dictionary.get(key))
                except AttributeError:
                    setattr(obj, key, dictionary.get(key))
        '''
        # old version, kept for reference
        #if a key represents an object (has a method 'load_internal_state') that method is called
        #this seems redundant, but otherwise there is no way of distinguishing between attribute that's an object and a dict
        if hasattr(obj, key):
            try:
                getattr(obj, key).load_internal_state(dictionary.get(key))
            except AttributeError:
                setattr(obj, key, dictionary.get(key))
        '''


def save_object_internal_state_to_dict(obj, *keys):
    """
    :param obj: an object whose internal state is to be saved
    :param keys: names of attributes that will be saved (if found),
                dicts can be passed to iterate over nested attributes
    :return: dict of saved attributes {'attr_name': attr_value}
    """
    if keys:
        state_dict = {}
        for key in keys:
            # iterate over passed arguments
            if isinstance(key, dict):
                # if passed argument is a dictionary we expect underlying attribute to be a complex object
                for _key in key.keys():
                    if hasattr(obj, _key):
                        state_dict[_key] = save_object_internal_state_to_dict(getattr(obj, _key), key[_key])
            else:
                if isinstance(key, tuple):
                    # unpack attributes from tuples
                    state_dict.update(save_object_internal_state_to_dict(obj, *key))
                elif hasattr(obj, key):
                    # check if object has an attribute, otherwise we ignore it
                    state_dict[key] = getattr(obj, key)
        return state_dict
    else:
        # if no keys were passed we try a default_save function
        try:
            return obj.default_save()
        except AttributeError:
            # if it doesn't exist return empty dict
            return {}


if __name__ == '__main__':

    class Obj1:
        def __init__(self, z):
            self.z = z

        def default_save(self):
            return save_object_internal_state_to_dict(self, 'z')

        def __str__(self):
            return 'Obj1: ' + str(self.z) + ', '


    class Obj2:
        def __init__(self, x, y):
            self.x, self.y = x, Obj1(y)

        def default_save(self):
            return save_object_internal_state_to_dict(self, 'x', {'y': ()})

        def __str__(self):
            return 'Obj2: ' + str(self.x) + ' ' + str(self.y) + ', '


    class Obj3:
        def __init__(self, attr1, x, y, z):
            self.attr1 = attr1
            self.attr2 = Obj1(z)
            self.attr3 = Obj2(x, y)

        def default_save(self):
            return save_object_internal_state_to_dict(self, 'attr1')

        def __str__(self):
            return 'Obj3: ' + str(self.attr1) + '  ' + str(self.attr2) + ' ' + str(self.attr3)


    obj = Obj3(3, 1, 2, 7)
    dictionary = save_object_internal_state_to_dict(obj, (), {'attr2': ()}, {'attr3': ()})
    print(dictionary)
    print(obj)
    print("small change")
    obj = Obj3(4, 2, 3, 8)
    print(obj)
    print('trying to revert changes...')
    load_object_internal_state_from_dict(obj, dictionary)
    print(obj)