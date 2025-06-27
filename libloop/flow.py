from itertools import islice, chain, takewhile, dropwhile
from typing import Iterable, Callable, TypeVar, Generator, Optional, Any, Union
from concurrent.futures import ThreadPoolExecutor

# Optional NumPy import for vectorized support
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

T = TypeVar('T')
S = TypeVar('S')

class Flow:
    """
    Composable, lazy iterable processing pipeline (similar to functional streams).
    Supports parallel and vectorized mapping with optional flags.
    Not thread-safe by design; use caution in concurrent contexts.
    """
    def __init__(self, iterable: Iterable[T]):
        # Avoid double-wrapping flows
        if isinstance(iterable, Flow):
            self.iterable = iterable.iterable
        else:
            self.iterable = iterable

    def sift(self, fn: Callable[[T], bool]) -> 'Flow[T]':
        """Filter elements using predicate fn(x)."""
        return Flow(x for x in self.iterable if fn(x))

    def morph(
        self, 
        fn: Callable[[Union[T, 'np.ndarray']], Union[S, 'np.ndarray']], 
        parallel: bool = False, 
        vectorized: bool = False, 
        max_workers: Optional[int] = None
    ) -> 'Flow[S]':
        """
        Map elements using fn(x).
        Optionally, map in parallel or in vectorized (NumPy) mode.
        Use only one of parallel or vectorized at a time.

        Args:
            fn: function to apply
            parallel: use ThreadPoolExecutor to apply fn concurrently
            vectorized: use NumPy to apply fn in batch (numeric types only)
            max_workers: number of threads if parallel=True

        Returns:
            New Flow of mapped items
        """
        if vectorized:
            if not HAS_NUMPY:
                raise ImportError("NumPy is not installed. Install it or use vectorized=False.")
            # Convert to NumPy array (works for most numeric iterables)
            arr = np.array(list(self.iterable))
            # If fn is vectorized, apply directly
            result = fn(arr)
            # If result is a NumPy array, wrap as Flow; else treat as iterable
            return Flow(result if isinstance(result, np.ndarray) else list(result))
        elif parallel:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Eager evaluation required for parallelism
                return Flow(list(executor.map(fn, self.iterable)))
        else:
            return Flow(fn(x) for x in self.iterable)

    def drip(self, n: int) -> 'Flow[T]':
        """Take first n elements."""
        return Flow(islice(self.iterable, n))

    def shed(self, n: int) -> 'Flow[T]':
        """Skip first n elements."""
        def generator():
            it = iter(self.iterable)
            for _ in range(n):
                next(it, None)
            yield from it
        return Flow(generator())

    def join(self, *others: Iterable[T]) -> 'Flow[T]':
        """Chain this flow with other iterables."""
        return Flow(chain(self.iterable, *others))

    def tap(self, fn: Callable[[T], Any]) -> 'Flow[T]':
        """Call fn(x) for each element, passing through the original value."""
        def generator():
            for x in self.iterable:
                fn(x)
                yield x
        return Flow(generator())

    def takewhile(self, predicate: Callable[[T], bool]) -> 'Flow[T]':
        """Take elements while predicate(x) is true."""
        return Flow(takewhile(predicate, self.iterable))

    def dropwhile(self, predicate: Callable[[T], bool]) -> 'Flow[T]':
        """Drop elements while predicate(x) is true, then yield the rest."""
        return Flow(dropwhile(predicate, self.iterable))

    def list(self) -> list:
        """Materialize the flow as a list."""
        return list(self.iterable)

    def to_list(self) -> list:
        """Alias for list()."""
        return self.list()

    def __iter__(self):
        return iter(self.iterable)

    def __repr__(self):
        # Show a preview of up to 5 elements for debugging
        preview = list(islice(self.iterable, 5))
        cls = self.__class__.__name__
        return f"<{cls} preview={preview}{'...' if len(preview) == 5 else ''}>"