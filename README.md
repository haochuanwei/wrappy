# wrappy
Decorators for common develop utilities.

# Usage
```Python
@probe()
def do_some_heavy_computation(a, b, c):
    return a * b + c

@probe()
def someone_elses_code():
    # code that does not explain itself
    #
    # A
    # HHHUUUUGGGGGEEEEE
    # MESS

@guard()
def play_with_fire():
    return 1 / 0

@todo()
def i_am_not_ready():
    pass

@guard()
@memoization()
def recursive_or_dynamic_programming_subroutine(n):
    assert isinstance(n, int) and n >= 0
    if n == 0:
        return 0
    return n + recursive_or_dynamic_programming_subroutine(n-1)
```