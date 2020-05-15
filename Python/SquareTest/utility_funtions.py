def abs_distance(x, y):
    """
    :return: absolute distance between x and y points
    """
    if x is not None and y is not None:
        return ((x[0]-y[0])**2 + (x[1] - y[1])**2)**0.5
    else:
        return 0


def distance_xy(from_, to_):
    if from_ is not None and to_ is not None:
        return to_[0]-from_[0], to_[1]-from_[1]
    else:
        return 0, 0


def load_object_internal_state_from_dict(obj, dictionary):
    """
    if a key represents simple variable then it's value is directly loaded
    if a key represents an object (has a method 'load_internal_state') that method is called
        this seems redundant, but otherwise there is no way of distinguishing between attribute that's an object and dict
    """
    for key in dictionary.keys():
        if hasattr(obj, key):
            try:
                getattr(obj, key).load_internal_state(dictionary.get(key))
            except AttributeError:
                setattr(obj, key, dictionary.get(key))


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
