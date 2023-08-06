"""Compute intensive module."""

from functools import lru_cache

# @lru_cache
def fib(n: int) -> int:
    if n < 1:
        return 0
    if n == 1:
        return 1
    return fib(n-1) + fib(n-2)
