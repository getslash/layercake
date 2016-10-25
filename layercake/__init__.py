from contextlib import contextmanager
from copy import deepcopy
from munch import munchify, unmunchify
import functools

__all__ = ['LayerCake']


class _Frosting(object):
    __slots__ = ['_obj']

    def __init__(self, obj):
        super(_Frosting, self).__init__()
        self._obj = obj

    def __getattr__(self, k):
        try:
            return super(_Frosting, self).__getattr__(k)
        except AttributeError:
            return getattr(self._obj, k)

    def __getitem__(self, k):
        return self._obj[k]


class LayerCake(object):
    def __init__(self, **default):
        super(LayerCake, self).__init__()
        if not default:
            raise ValueError("Can't create empty configuration")
        self._stack = [munchify(default)]
        self._allowed_keys = frozenset(self._stack[-1])

    def __str__(self):
        return 'LayerCake{}'.format([unmunchify(x) for x in reversed(self._stack)])
    __repr__ = __str__

    def push(self, **overrides):
        if not overrides:
            raise ValueError("Can't push empty configuration")
        if not self._allowed_keys.issuperset(set(overrides)):
            raise ValueError("Can't add new configuration keys")
        updated_cfg = deepcopy(self._stack[-1])
        updated_cfg.update(overrides)
        self._stack.append(updated_cfg)

    def pop(self):
        if len(self._stack) == 1:
            raise IndexError("Can't pop last configuration")
        return self._stack.pop()

    @contextmanager
    def overriding(self, **overrides):
        self.push(**overrides)
        try:
            yield self.current
        finally:
            self.pop()

    def with_overriding(self, **overrides):
        def dec(f):
            @functools.wraps(f)
            def wrapper(*args, **kwargs):
                with self.overriding(**overrides):
                    return f(*args, **kwargs)
            return wrapper
        return dec

    @property
    def current(self):
        return _Frosting(self._stack[-1])
