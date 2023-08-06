from objwrap import ClosedWrapper, wrapped


def test_closure():
    x = ClosedWrapper(1)
    y = ClosedWrapper(2)
    assert isinstance(x+y, ClosedWrapper)
    assert wrapped(x+y == 3)  # wrapped(...) retrieves the value

