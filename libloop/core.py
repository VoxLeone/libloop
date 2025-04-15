class Loop:
    def __init__(self, start, end, step=1):
        self.items = range(start, end, step)

    def print(self):
        for x in self.items:
            print(x)
        return self

    def map(self, func):
        self.items = map(func, self.items)
        return self

    def filter(self, func):
        self.items = filter(func, self.items)
        return self

    def for_each(self, func):
        for x in self.items:
            func(x)
        return self
