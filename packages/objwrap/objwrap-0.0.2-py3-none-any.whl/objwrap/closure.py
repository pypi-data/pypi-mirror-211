from objwrap.wrapper import Wrapper
from typing import Iterable
from collections.abc import Mapping


class Pending:
    def __init__(self, method, args, kwargs):
        self.method = method
        self.args = args
        self.kwargs = kwargs

    def __len__(self):
        return 3

    def __iter__(self):
        yield self.method
        yield self.args
        yield self.kwargs


class ClosedWrapper(Wrapper):
    def __before__(self, method, args, kwargs):
        args = [
            arg.__value__() if arg.__class__ == self.__class__ else arg for arg in args
        ]
        kwargs = {
            k: arg.__value__() if arg.__class__ == self.__class__ else arg
            for k, arg in kwargs.items()
        }
        return Pending(method, args, kwargs)

    def __unknown__(self, obj, name, args, kwargs):
        raise NotImplemented("Implement the __unknown__ fallback of __before__")

    def __after__(self, obj):
        return self.__class__(obj)

    def _wrapmethodcall(self, data):
        if isinstance(data, Pending):
            method, args, kwargs = data.method, data.args, data.kwargs
            return method(*args, **kwargs)
        if isinstance(data, Mapping):
            return {k: self._wrapmethodcall(v) for k, v in data.items()}
        if isinstance(data, Iterable):
            return (self._wrapmethodcall(v) for v in data)
        raise Exception(
            f"Invalid _wrapmethodcall unpacking for type {type(data)}. Fix the outputs of __before__ or __unknown__"
        )

    def __wrapattr__(self, obj, name):
        try:
            ret = super().__wrapattr__(obj, name)
            if not callable(ret):
                return ret
        except AttributeError:
            ret = None

        def method(*args, **kwargs):
            pending = (
                self.__unknown__(self.__value__(), name, args, kwargs)
                if ret is None
                else self.__before__(ret, args, kwargs)
            )
            if (
                not isinstance(pending, Pending)
                and not isinstance(pending, Mapping)
                and not isinstance(pending, Iterable)
            ):
                pending = Pending(*pending)
            result = self._wrapmethodcall(pending)
            return self.__after__(result)

        return method
