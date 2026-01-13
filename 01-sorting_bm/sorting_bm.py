import random
import timeit

from typing import Callable


FG_GREEN = "\x1b[32m"
FG_RST = "\x1b[0m"


def insertion_sort(data: list[int]) -> list[int]:
    """Sort data using insertion sort and return a new list."""
    arr = list(data)
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def _merge(left: list[int], right: list[int]) -> list[int]:
    """Merge two sorted lists into one sorted list."""
    merged: list[int] = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    if i < len(left):
        merged.extend(left[i:])
    if j < len(right):
        merged.extend(right[j:])

    return merged


def merge_sort(data: list[int]) -> list[int]:
    """Sort data using merge sort and return a new list."""
    arr = list(data)
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def timsort_builtin(data: list[int]) -> list[int]:
    """Sort data using Python's built-in sorting (Timsort)."""
    return sorted(data)


def gen_random(n: int) -> list[int]:
    """Generate random dataset."""
    # Use a wider value range to reduce accidental long runs of sorted values.
    return [random.randrange(0, n * 10 + 1) for _ in range(n)]


def gen_sorted(n: int) -> list[int]:
    """Generate already sorted dataset."""
    return list(range(n))


def gen_reversed(n: int) -> list[int]:
    """Generate reverse-sorted dataset."""
    return list(range(n, 0, -1))


def gen_nearly_sorted(n: int) -> list[int]:
    """Generate nearly sorted dataset by applying a several swaps."""
    arr = list(range(n))
    swaps = max(1, n // 100)  # ~1% of positions disturbed
    for _ in range(swaps):
        i = random.randrange(0, n)
        j = random.randrange(0, n)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


def gen_few_unique(n: int) -> list[int]:
    """Generate dataset with many duplicates (few unique values)."""
    val = max(2, int(n**0.5))
    return [random.randrange(0, val) for _ in range(n)]


def measure_ms_per_call(func: Callable[[list[int]], list[int]], data: list[int]) -> float:
    """Measure average ms per call using timeit, taking the best run.

    Args:
        func (Callable[[list[int]], list[int]): Tested function.
        data (list[int]): Input data (not mutated).

    Returns:
        float: Best observed average ms per single call.
    """
    # Choose timeit number parameter based on dataset size
    if len(data) <= 1000:
        number = 5
    elif len(data) <= 4000:
        number = 3
    else:
        number = 1

    timer = timeit.Timer(lambda: func(data))
    samples = timer.repeat(repeat=3, number=number)
    best_total = min(samples)
    return best_total / number * 1000


if __name__ == "__main__":
    print("BENCHMARK: sorting algorithms (best-of repeats).")
    print()

    sizes = [500, 1000, 2000, 4000, 8000]
    patterns = {
        "Random": gen_random,
        "Sorted": gen_sorted,
        "Reversed": gen_reversed,
        "Nearly sorted (~1% swaps)": gen_nearly_sorted,
        "Many duplicates (few unique)": gen_few_unique,
    }

    for pattern_name, gen in patterns.items():
        rows = []

        for n in sizes:
            data = gen(n)

            # Measure.
            t_ins = measure_ms_per_call(insertion_sort, data)
            t_merge = measure_ms_per_call(merge_sort, data)
            t_tim = measure_ms_per_call(timsort_builtin, data)

            rows.append((n, t_ins, t_merge, t_tim))

        # Print a simple aligned table
        print(f"{FG_GREEN}Dataset: {pattern_name}{FG_RST}")
        print(f"{'n':>7} | {'insertion ms':>12} | {'merge ms':>12} | {'timsort ms':>12}")
        print("-" * 52)
        for n, t_ins, t_merge, t_tim in rows:
            print(f"{n:7d} | {t_ins:>12.3f} | {t_merge:>12.3f} | {t_tim:>12.3f}")
        print()
