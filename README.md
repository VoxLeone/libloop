---

## 📘 `README.md` (Starter)

This is a work in progress.

---

# 🌀 Libloop

**LibLoop** is (at this point) a minimal abstraction over Python's `for` loops. It aims to make iteration cleaner, more expressive, and easier to compose — whether you're working with simple ranges or chaining functional operations like `map` and `filter`.

---

## 📦 Installation (dev mode)

```bash
git clone https://github.com/VoxLeone/libloop.git
cd libloop
pip install -e .
```

---

## 🚀 Quickstart

```python
from libloop import Loop

# Print numbers from 2 to 30 in steps of 3
Loop(2, 30, 3).print()

# Print squares of even numbers from 1 to 10
Loop(1, 10)
    .map(lambda x: x**2)
    .filter(lambda x: x % 2 == 0)
    .for_each(print)

#********While Loop*********

X = [0]

def condition():
    return x[0] < 5

def increment():
    x[0] += 1
    print(f"x = {x[0]}")

WhileLoop(condition).do(increment).run(delay=1)

#********DoWhileLoop*********
x = [0]

def increment():
    x[0] += 2
    print(f"x = {x[0]}")

DoWhileLoop().do(increment).until(lambda: x[0] > 5).run()

#********repeat_until loop********
count = [0]

repeat_until(
    condition_func=lambda: count[0] >= 3,
    action_func=lambda: (print("Hello"), count.__setitem__(0, count[0]+1)),
    delay=0.5
)

```

---

## 🎯 Goals

- ✅ Hide boilerplate `for` syntax
- ✅ Support easy printing
- ✅ Add map/filter/for_each methods
- ⏳ Collect results with `.to_list()`
- ⏳ Add support for other iterables (e.g. lists, sets)
- ⏳ Add parallel iteration options

---

## 🛠️ Dev Notes

Test with `pytest`:

```bash
pip install pytest
pytest
```

---

## 📝 License

MIT License. Use freely and make cool stuff.

---
