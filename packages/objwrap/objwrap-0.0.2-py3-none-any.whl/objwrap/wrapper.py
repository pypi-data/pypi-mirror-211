from objwrap.core import CustomWrapper


class Wrapper(CustomWrapper):
    def __init__(self, obj):
        super().__init__(obj, self)

    def __wrapattr__(self, obj, name):
        assert self.__value__() is obj
        return getattr(obj, name)
