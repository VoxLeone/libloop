---

## 📘 `README.md` (Starter)

This is a work in progress.

---
```markdown
# 🌀 Loopy

**Loopy** is a minimal abstraction over Python's `for` loops. It aims to make iteration cleaner, more expressive, and easier to compose — whether you're working with simple ranges or chaining functional operations like `map` and `filter`.

---

## 📦 Installation (dev mode)

```bash
git clone https://github.com/yourusername/loopy.git
cd loopy
pip install -e .
```

---

## 🚀 Quickstart

```python
from loopy import Loop

# Print numbers from 2 to 30 in steps of 3
Loop(2, 30, 3).print()

# Print squares of even numbers from 1 to 10
Loop(1, 10)
    .map(lambda x: x**2)
    .filter(lambda x: x % 2 == 0)
    .for_each(print)
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
```

---
