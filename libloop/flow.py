# libloop/flow.py

from itertools import islice, chain

class Flow:
    def __init__(self, iterable):
        self.iterable = iterable

    def sift(self, fn):
        return Flow(x for x in self.iterable if fn(x))

    def morph(self, fn):
        return Flow(fn(x) for x in self.iterable)

    def drip(self, n):
        return Flow(islice(self.iterable, n))

    def shed(self, n):
        def generator():
            it = iter(self.iterable)
            for _ in range(n):
                next(it, None)
            yield from it
        return Flow(generator())

    def join(self, *others):
        return Flow(chain(self.iterable, *others))

    def tap(self, fn):
        def generator():
            for x in self.iterable:
                fn(x)
                yield x
        return Flow(generator())

    def list(self):
        return list(self.iterable)

    def __iter__(self):
        return iter(self.iterable)
