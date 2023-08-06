class CustomWrapper:
    def __init__(self, obj, handler):
        self._obj = obj
        self._handler = handler

    def __value__(self):
        return self._obj

    def __wrapcall__(self, obj, name, *args, **kwargs):
        return self.__wrapattr__(obj, name)(*args, **kwargs)

    def __getattribute__(self, name):
        if name.startswith("_") or name in dir(self):
            return object.__getattribute__(self, name)
        return self._handler.__wrapattr__(self._obj, name)

    def __len__(self):
        return self._handler.__wrapcall__(self._obj, "__len__")

    def __iter__(self):
        return self._handler.__wrapcall__(self._obj, "__iter__")

    def __delitem__(self, name):
        return self._handler.__wrapcall__(self._obj, "__delitem__", name)

    def __getitem__(self, name):
        return self._handler.__wrapcall__(self._obj, "__getitem__", name)

    def __setitem__(self, name, value):
        return self._handler.__wrapcall__(self._obj, "__setitem__", name, value)

    def __abs__(self):
        return self._handler.__wrapcall__(self._obj, "__abs__")

    def __eq__(self, other):
        return self._handler.__wrapcall__(self._obj, "__eq__", other)

    def __lt__(self, other):
        return self._handler.__wrapcall__(self._obj, "__lt__", other)

    def __gt__(self, other):
        return self._handler.__wrapcall__(self._obj, "__gt__", other)

    def __le__(self, other):
        return self._handler.__wrapcall__(self._obj, "__le__", other)

    def __ge__(self, other):
        return self._handler.__wrapcall__(self._obj, "__ge__", other)

    def __ne__(self, other):
        return self._handler.__wrapcall__(self._obj, "__ne__", other)

    def __neg__(self):
        return self._handler.__wrapcall__(self._obj, "__neg__")

    def __add__(self, other):
        return self._handler.__wrapcall__(self._obj, "__add__", other)

    def __radd__(self, other):
        return self._handler.__wrapcall__(self._obj, "__add__", other)

    def __sub__(self, other):
        return self._handler.__wrapcall__(self._obj, "__sub__", other)

    def __rsub__(self, other):
        return self._handler.__wrapcall__(self._obj, "__rsub__", other)

    def __mul__(self, other):
        return self._handler.__wrapcall__(self._obj, "__mul__", other)

    def __rmul__(self, other):
        return self._handler.__wrapcall__(self._obj, "__rmul__", other)

    def __pow__(self, other):
        return self._handler.__wrapcall__(self._obj, "__pow__", other)

    def __rpow__(self, other):
        return self._handler.__wrapcall__(self._obj, "__rpow__", other)

    def __truediv__(self, other):
        return self._handler.__wrapcall__(self._obj, "__truediv__", other)

    def __rtruediv__(self, other):
        return self._handler.__wrapcall__(self._obj, "__rtruediv__", other)

    def __floordiv__(self, other):
        return self._handler.__wrapcall__(self._obj, "__floordiv__", other)

    def __rfloordiv__(self, other):
        return self._handler.__wrapcall__(self._obj, "__rfloordiv__", other)

    def __floor__(self):
        return self._handler.__wrapcall__(self._obj, "__floor__")

    def __ceil__(self):
        return self._handler.__wrapcall__(self._obj, "__ceil__")

    def __round__(self, n=None):
        return self._handler.__wrapcall__(self._obj, "__round__", n)

    def __float__(self):
        return self._handler.__wrapcall__(self._obj, "__float__")

    def __int__(self):
        return self._handler.__wrapcall__(self._obj, "__int__")

    def __bool__(self):
        return self._handler.__wrapcall__(self._obj, "__bool__")

    def __rshift__(self, other):
        return self._handler.__wrapcall__(self._obj, "__rshift__", other)

    def __lshift__(self, other):
        return self._handler.__wrapcall__(self._obj, "__lshift__", other)

    def __contains__(self, item):
        return self._handler.__wrapcall__(self._obj, "__lshift__", item)

    def __invert__(self):
        return self._handler.__wrapcall__(self._obj, "__invert__")

    def __matmul__(self, other):
        return self._handler.__wrapcall__(self._obj, "__matmul__", other)

    def __rmatmul__(self, other):
        return self._handler.__wrapcall__(self._obj, "__rmatmul__", other)

    def __or__(self, other):
        return self._handler.__wrapcall__(self._obj, "__or__", other)

    def __and__(self, other):
        return self._handler.__wrapcall__(self._obj, "__and__", other)

    def __ror__(self, other):
        return self._handler.__wrapcall__(self._obj, "__ror__", other)

    def __call__(self, *args, **kwargs):
        return self._handler.__wrapcall__(self._obj, "__call__", *args, **kwargs)

    def __str__(self):
        return self._handler.str(self._obj, "__str__")

    def __repr__(self):
        return self._handler.__wrapcall__(self._obj, "__repr__")
