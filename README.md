# libloop

**libloop** is a Python library for composable, flexible, and efficient iteration patterns.  It provides object-oriented and functional abstractions for classic loops (`for`, `while`, `do-while`), as well as a powerful, lazy, chainable flow API.

## Features

- **Loop Classes:**  
  OOP wrappers for `for`, `while`, and `do-while` constructs with chainable methods.
- **Functional Utilities:**  
  `repeat_until` for concise loop logic.
- **Lazy, Chainable Flow API:**  
  The `Flow` class for building composable, memory-efficient pipelines.
- **Parallelism:**  
  Opt-in parallel execution for mapping, filtering, and for-each using threads.
- **Vectorization:**  
  Opt-in vectorized mapping/filtering for numeric data (requires NumPy).
- **Thread Safety:**  
  Internal state is protected for safe use in concurrent scenarios (user code must still be thread-safe).
- **Extensive Documentation & Type Hints:**  
  All classes and methods are documented for ease of use and maintenance.

---

## Installation

```bash
pip install libloop
```

**NumPy is optional.**  
Install it if you want to enable vectorized operations:

```bash
pip install numpy
```

---

## Usage

### Loop Classes

```python
from libloop import Loop, WhileLoop, DoWhileLoop, repeat_until

# For-like loop with chaining
Loop(0, 10).map(lambda x: x * 2).filter(lambda x: x > 5).for_each(print)

# While loop with actions
counter = {'val': 0}
def action():
    counter['val'] += 1
WhileLoop(lambda: counter['val'] < 5).do(action).run()

# Do-while loop
n = {'val': 0}
def inc(): n['val'] += 2
def cond(): return n['val'] >= 6
DoWhileLoop().do(inc).until(cond).run()

# Functional repeat_until
x = {'val': 0}
repeat_until(lambda: x['val'] > 3, lambda: x.update(val=x['val'] + 1))
```

### Flow API

```python
from libloop.flow import Flow

# Lazy, composable pipelines
result = (
    Flow(range(100))
    .sift(lambda x: x % 3 == 0)
    .morph(lambda x: x + 1)
    .drip(10)
    .list()
)
print(result)
```

### Parallel and Vectorized Operations

```python
import numpy as np
from libloop import Loop
from libloop.flow import Flow

# Parallel mapping (using threads)
Loop(0, 100).map(lambda x: x**2, parallel=True).for_each(print)

# Vectorized mapping (NumPy required)
Loop(0, 10).map(lambda arr: arr * 3, vectorized=True).for_each(print)

# Flow with vectorized morph
Flow(range(10)).morph(lambda arr: arr ** 2, vectorized=True).tap(print).list()
```

---

## API Reference

- **Loop(start, end, step=1)**
  - `.map(func, parallel=False, vectorized=False, max_workers=None)`
  - `.filter(func, parallel=False, vectorized=False, max_workers=None)`
  - `.for_each(func, parallel=False, vectorized=False, max_workers=None)`
  - `.print()`
- **WhileLoop(condition_func)**
  - `.do(action_func)`
  - `.run(delay=0, max_iterations=None, parallel=False, max_workers=None)`
- **DoWhileLoop()**
  - `.do(action_func)`
  - `.until(condition_func)`
  - `.run(delay=0, max_iterations=None, parallel=False, max_workers=None)`
- **repeat_until(condition_func, action_func, delay=0, max_iterations=None, parallel=False, max_workers=None)**
- **Flow(iterable)**
  - `.sift(fn)`
  - `.morph(fn, parallel=False, vectorized=False, max_workers=None)`
  - `.drip(n)`
  - `.shed(n)`
  - `.join(*others)`
  - `.tap(fn)`
  - `.takewhile(predicate)`
  - `.dropwhile(predicate)`
  - `.list()`, `.to_list()`

---

## Thread Safety & Parallelism Notes

- Internal state of `Loop`, `WhileLoop`, and `DoWhileLoop` is thread-safe.
- User-supplied functions **must** be thread-safe if parallelism is enabled.
- `parallel=True` uses threads (good for I/O, general use).
- For CPU-bound work, process-based parallelism may be supported in future.
- `vectorized=True` requires NumPy and only works with numeric data.

---

## Contributing

Contributions, bug reports, and feature requests are welcome!  
See [issues](https://github.com/VoxleOne/libloop/issues).

---

## License

MIT License

---

## Acknowledgements

Inspired by Python’s built-in functional tools and modern data pipeline libraries.
