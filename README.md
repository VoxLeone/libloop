
# 🎒 `libloop`: Python Iterable Flow Toolkit

* **"Loop less. Flow more."**
---

## ⚠️ Heads up!

This repository is an open space for exploring experimental, weird, or half-baked concepts in code.
Things here might break, make no sense, or become something cool later. Or not.

If you're here out of curiosity, feel free to poke around or borrow anything useful. If you're expecting polished code or production readiness… this probably isn't the place (yet). 😄

---
## Rationale

We're building a Python library that:

    Abstracts loops behind chainable, declarative transformations

    Emphasizes flow-style processing like JavaScript's Symbol.iterator or functional pipelines

    Wraps iterable logic into a clean, expressive API: Flow(...).sift(...).morph(...).drip(...)

## 🧩 What Makes libloop Distinct?

    It's Pythonic, but inspired by FP-style chains (à la Lodash, RxJS, or LINQ)

    Encourages loop-free reasoning, which is rare in small Python libs

    Could serve as an expressive, lazy data pipeline tool, especially for devs tired of writing for-loops and if filters manually

---

### 🧱 Core Principles

* Declarative over imperative
* Chainable, fluent interface
* Named flows with clear intent (`.drip()`, `.sift()`, `.morph()`)
* Generator-based and lazy by default
* Plays nicely with `iter()`, `next()`, `for`, etc.

---

### 💡 Building Blocks

| Operation       | Description                           | Evocative Name   |
| --------------- | ------------------------------------- | ---------------- |
| `filter()`      | Keep only values matching a predicate | `.sift()`        |
| `map()`         | Transform each value                  | `.morph()`       |
| `take(n)`       | Take only first `n` items             | `.drip(n)`       |
| `skip(n)`       | Skip first `n` items                  | `.shed(n)`       |
| `flatten()`     | Unpack nested iterables               | `.spill()`       |
| `unique()`      | Remove duplicates                     | `.distinct()`    |
| `window(n)`     | Sliding window of `n` values          | `.glimpse(n)`    |
| `enumerate()`   | Yield `(index, value)`                | `.counted()`     |
| `zip(other)`    | Combine with another iterable         | `.braid(other)`  |
| `reduce()`      | Fold into a single value              | `.forge(fn)`     |
| `chain(*iters)` | Concatenate iterables                 | `.join(*others)` |
| `peek(fn)`      | Run side-effect fn (for debugging)    | `.tap(fn)`       |

---

### 🧪 Example Usage

```python
from libloop import Flow

flow = (
    Flow(range(20))
    .shed(5)             # skip first 5
    .sift(lambda x: x % 2 == 0)   # keep evens
    .morph(lambda x: x * 10)
    .drip(4)             # take first 4 of these
)

for val in flow:
    print(val)  # 60, 80, 100, 120
```

Or for composition:

```python
values = Flow(range(1, 11)).distinct().morph(str).join(['end']).list()
print(values)  # ['1', '2', ..., '10', 'end']
```

---

### 🧰 Starter Code Skeleton

```python
class Flow:
    def __init__(self, iterable):
        self.iterable = iterable

    def sift(self, fn):
        return Flow(x for x in self.iterable if fn(x))

    def morph(self, fn):
        return Flow(fn(x) for x in self.iterable)

    def drip(self, n):
        def take():
            count = 0
            for x in self.iterable:
                if count < n:
                    yield x
                    count += 1
                else:
                    break
        return Flow(take())

    def shed(self, n):
        def skip():
            it = iter(self.iterable)
            for _ in range(n):
                next(it, None)
            yield from it
        return Flow(skip())

    def join(self, *others):
        from itertools import chain
        return Flow(chain(self.iterable, *others))

    def list(self):
        return list(self.iterable)

    def __iter__(self):
        return iter(self.iterable)
```

---

### 🛠 Ideas for Expansion

* Add `async` support: `AsyncFlow`
* Integrate with pandas or NumPy for dataframe-like ops
* Debug chain visualizer: `.trace()` that prints each stage
* Custom exceptions for bad patterns (e.g., `.drip(-1)`)

---

## 📝 License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

MIT License. Use freely and make cool stuff.

---
