import time
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Optional, Iterable, Any

# Try importing numpy. Will be used only if vectorized=True.
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

class Loop:
    """
    An enhanced for-like loop with map, filter, and for_each operations.
    Supports parallelization and vectorization with optional flags.
    Thread safety is provided for internal state (`self.items`).
    """
    def __init__(self, start: int, end: int, step: int = 1):
        self._lock = threading.Lock()
        self.items = range(start, end, step)

    def print(self):
        """Print all items in the loop."""
        with self._lock:
            for x in self.items:
                print(x)
        return self

    def map(self, func: Callable, parallel: bool = False, vectorized: bool = False, max_workers: Optional[int] = None):
        """
        Apply `func` to all items. Supports parallel and vectorized execution.

        Args:
            func: Function to apply.
            parallel: If True, apply in parallel using threads.
            vectorized: If True, use numpy for vectorized mapping (numeric types only).
            max_workers: Number of threads (if parallel=True).
        """
        with self._lock:
            # Vectorized mapping using numpy
            if vectorized:
                if not HAS_NUMPY:
                    raise ImportError("NumPy is not installed. Install it or use vectorized=False.")
                if not isinstance(self.items, (np.ndarray, list, range)):
                    raise TypeError("Vectorized map requires a list, range, or numpy array.")
                arr = np.array(self.items)
                # Assume func is vectorized or can operate on numpy arrays
                self.items = func(arr)
                return self
            # Parallel mapping using threads
            elif parallel:
                # Convert to list for repeated access
                items = list(self.items)
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    results = list(executor.map(func, items))
                self.items = results
                return self
            # Sequential mapping
            else:
                self.items = list(map(func, self.items))
                return self

    def filter(self, func: Callable, parallel: bool = False, vectorized: bool = False, max_workers: Optional[int] = None):
        """
        Filter items by a function. Supports parallel and vectorized execution.

        Args:
            func: Predicate function.
            parallel: If True, filter in parallel using threads.
            vectorized: If True, use numpy for vectorized filtering.
            max_workers: Number of threads (if parallel=True).
        """
        with self._lock:
            if vectorized:
                if not HAS_NUMPY:
                    raise ImportError("NumPy is not installed. Install it or use vectorized=False.")
                arr = np.array(self.items)
                mask = func(arr)  # Should return a boolean array
                self.items = arr[mask]
                return self
            elif parallel:
                items = list(self.items)
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    results = list(executor.map(func, items))
                self.items = [item for item, keep in zip(items, results) if keep]
                return self
            else:
                self.items = list(filter(func, self.items))
                return self

    def for_each(self, func: Callable, parallel: bool = False, vectorized: bool = False, max_workers: Optional[int] = None):
        """
        Apply a function to each item. Supports parallel and vectorized execution.

        Args:
            func: Function to apply (should not return a value).
            parallel: If True, run in parallel using threads.
            vectorized: If True, use numpy for vectorized action.
            max_workers: Number of threads (if parallel=True).
        """
        with self._lock:
            if vectorized:
                if not HAS_NUMPY:
                    raise ImportError("NumPy is not installed. Install it or use vectorized=False.")
                arr = np.array(self.items)
                func(arr)
                return self
            elif parallel:
                items = list(self.items)
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    list(executor.map(func, items))
                return self
            else:
                for x in self.items:
                    func(x)
                return self


class WhileLoop:
    """
    A while-loop abstraction supporting multiple actions, delays, and max iterations.
    Thread safety is provided for internal state (`self.actions`).
    """
    def __init__(self, condition_func: Callable[[], bool]):
        self.condition_func = condition_func
        self._lock = threading.Lock()
        self.actions = []

    def do(self, action_func: Callable[[], None]):
        """Register an action to perform each iteration."""
        with self._lock:
            self.actions.append(action_func)
        return self

    def run(self, delay: float = 0, max_iterations: Optional[int] = None, parallel: bool = False, max_workers: Optional[int] = None):
        """
        Run the while loop.

        Args:
            delay: Time to sleep between iterations (seconds).
            max_iterations: Max number of iterations.
            parallel: If True, run all actions in parallel each iteration.
            max_workers: Number of threads (if parallel=True).
        """
        count = 0
        while self.condition_func():
            with self._lock:
                actions = list(self.actions)
            if parallel:
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    list(executor.map(lambda f: f(), actions))
            else:
                for action in actions:
                    action()
            if delay > 0:
                time.sleep(delay)
            count += 1
            if max_iterations and count >= max_iterations:
                break
        return self


class DoWhileLoop:
    """
    A do-while-loop abstraction supporting multiple actions, delays, and max iterations.
    Thread safety is provided for internal state (`self.actions`).
    """
    def __init__(self):
        self._lock = threading.Lock()
        self.actions = []
        self.condition_func = lambda: False

    def do(self, action_func: Callable[[], None]):
        """Register an action to perform each iteration."""
        with self._lock:
            self.actions.append(action_func)
        return self

    def until(self, condition_func: Callable[[], bool]):
        """Set the condition for loop exit."""
        self.condition_func = condition_func
        return self

    def run(self, delay: float = 0, max_iterations: Optional[int] = None, parallel: bool = False, max_workers: Optional[int] = None):
        """
        Run the do-while loop.

        Args:
            delay: Time to sleep between iterations (seconds).
            max_iterations: Max number of iterations.
            parallel: If True, run all actions in parallel each iteration.
            max_workers: Number of threads (if parallel=True).
        """
        count = 0
        while True:
            with self._lock:
                actions = list(self.actions)
            if parallel:
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    list(executor.map(lambda f: f(), actions))
            else:
                for action in actions:
                    action()
            count += 1
            if delay > 0:
                time.sleep(delay)
            if self.condition_func():
                break
            if max_iterations and count >= max_iterations:
                break
        return self


def repeat_until(condition_func: Callable[[], bool], action_func: Callable[[], None], delay: float = 0, max_iterations: Optional[int] = None, parallel: bool = False, max_workers: Optional[int] = None):
    """
    Repeat action_func until condition_func returns True.

    Args:
        condition_func: Function returning a bool to determine when to stop.
        action_func: Action to repeat.
        delay: Time to sleep between repetitions (seconds).
        max_iterations: Max number of repetitions.
        parallel: If True and action_func is iterable, runs actions in parallel.
        max_workers: Number of threads (if parallel=True).
    """
    count = 0
    if parallel and hasattr(action_func, "__iter__"):
        # If action_func is iterable, run all in parallel each repetition
        while not condition_func():
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                list(executor.map(lambda f: f(), action_func))
            count += 1
            if delay > 0:
                time.sleep(delay)
            if max_iterations and count >= max_iterations:
                break
    else:
        while not condition_func():
            action_func()
            count += 1
            if delay > 0:
                time.sleep(delay)
            if max_iterations and count >= max_iterations:
                break