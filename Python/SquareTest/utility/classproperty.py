
class class_property(property):

    def __get__(self, obj, objtype=None):
        return super(class_property, self).__get__(objtype)

    def __set__(self, obj, value):
        super(class_property, self).__set__(type(obj), value)

    def __delete__(self, obj):
        super(class_property, self).__delete__(type(obj))
