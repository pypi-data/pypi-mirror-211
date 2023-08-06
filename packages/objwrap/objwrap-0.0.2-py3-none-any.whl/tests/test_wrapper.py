from objwrap import Wrapper


def test_numeric_wrap():
    x = Wrapper(1)
    assert x+1 == 2
    assert x-1 == 0
    assert x*2 == 2
    assert x/2 == 0.5
    assert x//2 == 0
    assert 2*x == 2
    assert x**2 == 1
    assert 2**x == 2
    assert x >> 1 == 0
    assert x << 1 == 2
    assert int(x) == 1
    assert float(x) == 1
    assert bool(x)
