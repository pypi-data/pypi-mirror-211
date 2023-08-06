from objwrap.wrapper import Wrapper
from typing import Iterable
from collections.abc import Mapping

class _Future(tuple):
    pass


class ClosedWrapper(Wrapper):
    def __before__(self, method, args, kwargs):
        args = [arg.__value__() if arg.__class__ == self.__class__ else arg for arg in args]
        kwargs = {k: arg.__value__() if arg.__class__ == self.__class__ else arg for k, arg in kwargs.items()}
        return method, args, kwargs

    def __after__(self, obj):
        return self.__class__(obj)

    def _wrapmethodcall(self, data):
        if isinstance(data, _Future):
            method, args, kwargs = data
            return method(*args, **kwargs)
        if isinstance(data, Mapping):
            return {k: self.__wrapmethodcall__(v) for k, v in data.items()}
        if isinstance(data, Iterable):
            return (self.__wrapmethodcall__(v) for v in data)
        raise Exception(f"Invalid _wrapmethodcall unpacking for type {type(data)}. Fix the outputs of __before__")

    def __wrapattr__(self, obj, name):
        ret = super().__wrapattr__(obj, name)
        if not callable(ret):
            return ret

        def method(*args, **kwargs):
            called_method, args, kwargs = self.__before__(ret, args, kwargs)
            result = self._wrapmethodcall(_Future((called_method, args, kwargs)))
            return self.__after__(result)
        return method
