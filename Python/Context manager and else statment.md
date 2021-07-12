# Context manager and Else statement
## Else
* for else: when loop stops without break
    ```python
    for item in my_list:
        if item.flavor == 'banana':
            break
    else:
        raise ValueError("No banana found")
    ```
* try else: when no exceptions throws
    ```python
    try:
        dangerous_call()
    except OSError:
        log()
    else:
        after_call()
    ```
    EAFP( Easier to ask for forgiveness than permission) vs LBYL (Look before you leap) 风格

##  `__exit__` method:
``` python
def __exit__(self, exc_type, exc_value, traceback):
    close_something()
    if exc_type is ZeroDivisionError:
        log()
        return Tru # ZeroDivisionError surpressed
```
**Python will defaultly throw the exception: If `__exit__` returns `None`, or anything other than `True`, the exception will propagate back**


##  Tools in `contextlib`
* `closing`: when target implemented `close()`, it's equivalent to
    ``` python
    from contextlib import contextmanager

    @contextmanager
    def closing(thing):
        try:
            yield thing
        finally:
            thing.close()
    ```
* `surpress`: ignore a specific exception in the body, example:
  ```python
    from contextlib import suppress

    with suppress(FileNotFoundError):
        os.remove('somefile.tmp')
  ```

* `class contextlib.ContextDecorator`: A base class that enables a context manager to also be used as a decorator.
    ```python
    from contextlib import ContextDecorator

    class mycontext(ContextDecorator):
        def __enter__(self):
            print('Starting')
            return self

        def __exit__(self, *exc):
            print('Finishing')
            return False

    >>> @mycontext()
    ... def function():
    ...     print('The bit in the middle')
    ...
    >>> function()
    Starting
    The bit in the middle
    Finishing
    ```
* `@contextmanager`
标准写法:
```python
import contextlib

@contextlib.contextmanager
def foo():
    something = do_something()
    try:
        yield something
    except Exception:
        handle_exceptions_in_with_body()
    finally:
        clean_up()
```
**Python will defaultly surpress exception: if you want it to throw, manually raise it**






