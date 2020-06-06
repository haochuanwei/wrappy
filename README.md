# wrappy
Decorators for common developer utilities in Python 3.6+.

## Documentation
Documentation is built with Mkdocs and hosted [here](https://erniethornhill.github.io/wrappy/).

## Quick Examples (see the docs for more detail)
```Python
from wrappy import probe, guard, todo, memoize

@probe()
def do_some_heavy_computation(a, b, c):
    return a * b + c

@probe(show_args=True, show_kwargs=True, show_returns=True)
def someone_elses_code():
    # code that does not explain itself
    #
    # show examples of args, kwargs, and return values at runtime to get some clue

@probe(show_caller=5)
def a_call_chain_would_be_nice():
    # find out with show_caller=<number_of_callers_along_the_chain>

@guard(fallback_retval=0)
def this_could_blow_up(a, b):
    return a / b

@todo('Not implemented')
def i_am_not_ready():
    # code is under construction, so throw an error when called prematurely

@guard()
@memoize()
def recursive_or_dynamic_programming_subroutine(n):
    assert isinstance(n, int) and n >= 0
    if n == 0:
        return 0
    return n + recursive_or_dynamic_programming_subroutine(n-1)
```

## Examples by Comparison

`This section is under construction!`

## Release Notes
