'''
Decorators for common Python developer utility.
'''
from functools import wraps
from collections import OrderedDict
from time import time
from pprint import pformat
import inspect
import wasabi
import traceback
import random
import json

logger = wasabi.Printer()
INFO_COLOR = "blue"
THEME_COLORS = ["green", "black", "red", "cyan", "yellow"]

def probe(show_caller=True, show_args=True, show_kwargs=True, show_returns=True, random_theme=True):
    """
    Tracks the running time of a function.
    Optionally also shos its caller, args, kwargs, and return value.
    Compatible with Python's multiprocess module due to functools.wraps.
    Works on functions and methods.

    Usage:
    @probe()
    def foo():
        # do stuff

    @other_decorator
    @probe(show_caller=2) # to find the true caller beyond other_decorator
    def bar():
        # do more stuff
    """
    # random color theme produces better distinguishment between different probes
    # which becomes relevant when probing along a call chain
    if random_theme:
        fore_color = "white"
        back_color = random.choice(THEME_COLORS)
        if random.uniform(0, 1) < 0.5:
            fore_color, back_color = back_color, fore_color
    else:
        fore_color = "white"
        back_color = THEME_COLORS[0]

    def wrapper(func):
        @wraps(func)
        def probed_func(*args, **kwargs):
            func_name = wasabi.color(func.__qualname__, fg=fore_color, bg=back_color, bold=True)
            module_name = wasabi.color(func.__module__, fg=fore_color, bg=back_color, bold=True)
            logger.divider(f"Probing {func_name}")
            logger.divider(f"From module {module_name}", char='_')

            if show_caller:
                caller_max_level = show_caller if isinstance(show_caller, int) else 1
                caller_names = [get_caller_name(k+3) for k in range(caller_max_level)]
                logger.divider(f"{func_name} caller", char='-')
                for i, _caller_name in enumerate(caller_names):
                    format_caller_name = wasabi.color(_caller_name, fg=INFO_COLOR, bold=True)
                    logger.text(f"Level {i+1} {format_caller_name}")

            if show_args:
                args_zip= zip(inspect.getargspec(func).args, args)
                format_args = dict()
                for _arg_name, _arg_value in args_zip:
                    format_args[wasabi.color(_arg_name, fg=INFO_COLOR, bold=True)] = pformat(_arg_value)
                logger.divider(f"{func_name} args", char='-')
                print(wasabi.table(format_args))

            if show_kwargs:
                format_kwargs = dict()
                for _kwarg_name, _kwarg_value in kwargs.items():
                    format_kwargs[wasabi.color(_kwarg_name, fg=INFO_COLOR, bold=True)] = pformat(_kwarg_value)
                logger.divider(f"{func_name} kwargs", char='-')
                print(wasabi.table(format_kwargs))

            logger.divider(f"{func_name} begins execution", char='-')
            tic = time()
            retval = func(*args, **kwargs)
            toc = time()
            logger.info(f"{func_name} running time: {toc - tic} seconds.")

            if show_returns:
                logger.divider(f"{func_name} returns", char='-')
                print(pformat(retval))

            logger.divider()
            return retval
        return probed_func
    return wrapper

def get_caller_name(skip=2):
    """
    Get a name of a caller in the format module.class.method.
    """
    stack = inspect.stack()
    if len(stack) < skip + 1:
        return ''
    parentframe = stack[skip][0]

    name = []
    module = inspect.getmodule(parentframe)
    if module:
        name.append(module.__name__)

    if 'self' in parentframe.f_locals:
        name.append(parentframe.f_locals['self'].__class__.__name__)
    codename = parentframe.f_code.co_name
    if codename != '<module>':
        name.append(codename)
    del parentframe
    return ".".join(name)

def todo(message="This functions is not yet implemented."):
    def wrapper(func):
        @wraps(func)
        def todo_func(*args, **kwargs):
            raise ValueError(message)
        return todo_func
    return wrapper

def guard(fallback_retval=0, fallback_func=None, print_traceback=False):
    '''
    Wraps a try-except block around a function, with a fallback return value or function.
    By default, there is no fallback function.
    The fallback function must be callable and will override the fallback value.
    Here's a trivial usage example:
    
    @guard(fallback_retval=0)
    def divide(a, b):
        return a / b
    '''
    # determine which fallback to use later
    if fallback_func is not None:
        assert callable(fallback_func), "Expected a callable as the fallback function."
        fallback = fallback_func
    else:
        def fallback(*args, **kwargs):
            return fallback_retval
        
    # construct the actual decorator
    def wrapper(func):
        @wraps(func)
        def guarded_func(*args, **kwargs):
            try:
                retval = func(*args, **kwargs)
            except Exception as e:
                logger.warn(f'Guarding function {func.__module}.{func.__qualname__}: suppressing {type(e)}: {e}')
                if print_traceback:
                    traceback.print_exc()
                retval = fallback(*args, **kwargs)
            finally:
                return retval
        return guarded_func
    return wrapper

def args_as_string(*args, **kwargs):
    '''
    Turn arguments and keyword arguments into a string representation.
    @param args: each member must support __repr__().
    @param kwargs: order-insensitive, each member must be serializable.
    '''
    args_str_form = ', '.join([_arg.__repr__() for _arg in args])
    kwargs_str_form = json.dumps(kwargs, ensure_ascii=False, sort_keys=True)
    return f'args: {args_str_form}, kwargs: {kwargs_str_form}'

def memoize(cache_limit=1000):
    '''
    Memoize the output of a function.
    Uses an OrderedDict for least-recently-used(LRU) caching.
    '''
    def wrapper(func):
        @wraps(func)
        memory = OrderedDict()
        def memoized_func(*args, **kwargs):
            lookup_key = args_as_string(*args, **kwargs)
            if lookup_key in memory:
                # if already memoized, refresh to the last-in position in the memory
                retval = memory[lookup_key]
                memory.move_to_end(lookup_key, last=True)
            else:
                # if not memoized, compute the value and store it in the memory
                retval = func(*args, **kwargs)
                memory[lookup_key] = retval
                # if memory if full, drop in a FIFO manner
                if len(memory.keys()) > cache_limit:
                    memory.popitem(last=False)
            return retval
        return memoized_func
    return wrapper
