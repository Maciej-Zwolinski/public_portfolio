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