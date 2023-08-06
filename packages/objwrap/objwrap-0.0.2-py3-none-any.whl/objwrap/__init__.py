from objwrap.wrapper import CustomWrapper
from objwrap.wrapper import Wrapper
from objwrap.closure import ClosedWrapper


def wrapped(obj):
    return obj.__value__()
