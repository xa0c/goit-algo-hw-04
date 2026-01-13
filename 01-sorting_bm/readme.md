# Comparison of Sorting Algorithms in Python

## Insertion sort

Insertion sort shows the expected _O(n^2)_ behavior on typical (random) data: as _n_ grows, runtime increases quadratically and becomes impractical for large arrays. However, its best-case _O(n)_ behavior is visible on sorted inputs, where it becomes faster than Merge sort. On partially sorted inputs it is competitive or even faster than Merge sort - but only at small sizes.

## Merge sort

Merge sort exhibits stable _O(n log n)_ scaling across all dataset types and remains feasible on larger arrays.

## Timsort (built-in `sorted` function)

Python's built-in sorting (`sorted`) is consistently the fastest in most scenarios. This is due to both:
- Timsort's algorithmic design: it is adaptive, detecting existing ordered runs and using insertion-sort-like behavior on small runs plus efficient merging, which yields near-linear behavior on partially ordered inputs.
- A highly optimized CPython implementation (written in C) with lower constant factors than Python-level implementations.

## Practical takeaway

The strongest practical advantage of Timsort is observable on datasets with existing structure (e.g., "chunk-sorted runs" or nearly sorted inputs), where its adaptivity reduces work compared to a generic merge sort, and it avoids the quadratic blow-up of insertion sort on disordered inputs.

Therefore, for production code, programmers typically rely on Python's built-in sorting rather than implementing sorting algorithms by hand: it is asymptotically efficient (_O(n log n)_ worst case), adaptive in practice, and heavily optimized.

## Benchmark results

```
Dataset: Random
      n | insertion ms |     merge ms |   timsort ms
----------------------------------------------------
    500 |        2.069 |        0.495 |        0.015
   1000 |       10.047 |        1.084 |        0.049
   2000 |       45.420 |        2.353 |        0.129
   4000 |      180.782 |        5.082 |        0.310
   8000 |      723.968 |       10.836 |        0.718

Dataset: Sorted
      n | insertion ms |     merge ms |   timsort ms
----------------------------------------------------
    500 |        0.024 |        0.379 |        0.002
   1000 |        0.058 |        0.814 |        0.003
   2000 |        0.123 |        1.720 |        0.006
   4000 |        0.252 |        3.627 |        0.013
   8000 |        0.508 |        7.672 |        0.027

Dataset: Reversed
      n | insertion ms |     merge ms |   timsort ms
----------------------------------------------------
    500 |        3.894 |        0.385 |        0.002
   1000 |       18.495 |        0.826 |        0.004
   2000 |       82.536 |        1.762 |        0.007
   4000 |      346.887 |        3.702 |        0.015
   8000 |     1419.621 |        7.764 |        0.030

Dataset: Nearly sorted (~1% swaps)
      n | insertion ms |     merge ms |   timsort ms
----------------------------------------------------
    500 |        0.112 |        0.413 |        0.005
   1000 |        0.327 |        0.899 |        0.009
   2000 |        1.327 |        1.995 |        0.020
   4000 |        5.287 |        4.243 |        0.045
   8000 |       19.553 |        9.266 |        0.110

Dataset: Many duplicates (few unique)
      n | insertion ms |     merge ms |   timsort ms
----------------------------------------------------
    500 |        2.131 |        0.480 |        0.014
   1000 |        9.977 |        1.038 |        0.032
   2000 |       42.960 |        2.246 |        0.094
   4000 |      184.870 |        4.833 |        0.240
   8000 |      727.540 |       10.474 |        0.549
```
