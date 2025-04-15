import time

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


class WhileLoop:
    def __init__(self, condition_func):
        self.condition_func = condition_func
        self.actions = []

    def do(self, action_func):
        self.actions.append(action_func)
        return self

    def run(self, delay=0, max_iterations=None):
        count = 0
        while self.condition_func():
            for action in self.actions:
                action()
            if delay > 0:
                time.sleep(delay)
            count += 1
            if max_iterations and count >= max_iterations:
                break
        return self


class DoWhileLoop:
    def __init__(self):
        self.actions = []
        self.condition_func = lambda: False

    def do(self, action_func):
        self.actions.append(action_func)
        return self

    def until(self, condition_func):
        self.condition_func = condition_func
        return self

    def run(self, delay=0, max_iterations=None):
        count = 0
        while True:
            for action in self.actions:
                action()
            count += 1
            if delay > 0:
                time.sleep(delay)
            if self.condition_func():
                break
            if max_iterations and count >= max_iterations:
                break
        return self


def repeat_until(condition_func, action_func, delay=0, max_iterations=None):
    count = 0
    while not condition_func():
        action_func()
        count += 1
        if delay > 0:
            time.sleep(delay)
        if max_iterations and count >= max_iterations:
            break

