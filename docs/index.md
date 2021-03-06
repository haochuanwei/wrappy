# Home

Decorators for common developer utilities in Python 3.6+.

For more information, please visit the project on [Github](https://github.com/haochuanwei/wrappy).

## Installation

```bash
pip install wrappy
```

## Usage

```python
import wrappy
```

### Investigate function/method behavior with ```@probe()```

```wrappy.probe()``` gives a decorator that prints information when the decorated function is called.
It primarily has the following options:

* show_caller (bool or int): whether to show the caller(s) and how many levels to show.
    - ```probe(show_caller=True)``` shows the immediate caller;
    - ```probe(show_caller=3)``` shows callers up to 3 levels up the stack.
* show_args (bool): whether to print positional arguments
* show_kwargs (bool): whether to print keyword arguments
* show_returns (bool): whether to print returned values

```Python
from wrappy import probe

@probe() # by default, probe() only tracks running time
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
```

### Fail-safe a function/method with ```@guard()```

```wrappy.guard()``` wraps a try-except block around the decorated function, and returns a specified value or function call when getting an exception.
It has the following options:

* fallback_retval (any): the return value to use when getting an exception .
* fallback_func (callable): the alternative function to call when getting an exception. If supplied, the fallback function must be callable and will override the fallback value. 
* print_traceback (bool): whether to show the traceback information when getting an exception.

```Python
from wrappy import guard

@guard(fallback_retval=0)
def this_could_blow_up(a, b):
    return a / b

@guard(fallback_func=local_robust_api)
def online_cool_api(*args):
    # make an HTTP request that could fail
```

### Easy memoization with ```@memoize()```

Using a least-recently-used(LRU) cache, store the return values of a function given a set of positional/keyword arguments passed to it. The following options are available:

* cache_limit (int): the size of the LRU cache in terms of sets of arguments, which is 1000 by default.

```Python
from wrappy import memoize, guard

@guard()
@memoize()
def recursive_or_dynamic_programming_subroutine(n):
    assert isinstance(n, int) and n >= 0
    if n == 0:
        return 0
    return n + recursive_or_dynamic_programming_subroutine(n-1)
```

### Prevent a function/method from running with ```@todo()```

This is self-explanatory -- ```@todo()``` denotes a function that is yet to be implemented, and no other code should call it. Using the decorator lets you place calls of this function in other code before finishing it, without leaving bugs behind.

```Python
@todo('Not implemented')
def i_am_not_ready():
    # code is under construction, so throw an error when called prematurely
```