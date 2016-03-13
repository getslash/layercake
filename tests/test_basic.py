from layercake import LayerCake
import pytest


@pytest.fixture
def lc():
    return LayerCake(a=1, b=2)


def test_assertions(lc):        # pylint: disable=redefined-outer-name
    with pytest.raises(ValueError):
        LayerCake()
    with pytest.raises(ValueError):
        lc.push()
    with pytest.raises(ValueError):
        lc.push(c=3)
    with pytest.raises(IndexError):
        lc.pop()


def test_current(lc):           # pylint: disable=redefined-outer-name
    assert lc.current.a == 1
    with lc.overriding(a=3) as current:
        assert current.a == 3
        with pytest.raises(AttributeError):
            current.a = 4
    assert current != lc.current
    assert lc.current.a == 1
    assert dict(**lc.current) == {'a': 1, 'b': 2}


def test_decorator(lc):
    assert lc.current.b == 2
    @lc.with_overriding(b=3)
    def wrapped():
        assert lc.current.b == 3
    assert lc.current.b == 2
    wrapped()
    assert lc.current.b == 2
